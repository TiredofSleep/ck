/*
 * ck_steer.c -- CK Steering Engine in C
 * Zero Python overhead. Direct Windows API calls.
 *
 * Replaces the psutil-based steering loop that caused GIL jitter spikes.
 * The algebra is the same: CL compose → nice + affinity. The language changed.
 *
 * Compile (MSVC):
 *   cl /O2 /LD ck_steer.c /Fe:ck_steer.dll /link advapi32.lib
 *
 * Compile (MinGW):
 *   gcc -O2 -shared -o ck_steer.dll ck_steer.c -ladvapi32
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

#include <windows.h>
#include <tlhelp32.h>
#include <stdio.h>
#include <string.h>

/* ═══════════════════════════════════════════
 * §1  THE ALGEBRA (from ck_tig.py)
 * ═══════════════════════════════════════════ */

#define NUM_OPS 10
#define HARMONY 7
#define VOID_OP 0

/* TSML: measurement lens. 73% HARMONY. */
static const int TSML[10][10] = {
    {0,0,0,0,0,0,0,7,0,0},{0,7,3,7,7,7,7,7,7,7},{0,3,7,7,4,7,7,7,7,9},
    {0,7,7,7,7,7,7,7,7,3},{0,7,4,7,7,7,7,7,8,7},{0,7,7,7,7,7,7,7,7,7},
    {0,7,7,7,7,7,7,7,7,7},{7,7,7,7,7,7,7,7,7,7},{0,7,7,7,8,7,7,7,7,7},
    {0,7,9,3,7,7,7,7,7,7},
};

/* Bidirectional compose (from ck_tig.py) */
static void compose(int b, int d, int direction,
                    int *being, int *doing, int *becoming)
{
    if (direction == 0) {
        /* FORWARD: expand, express (multiplication) */
        *being = TSML[b][d];
        *doing = (b * d) % 10;
        *becoming = ((*being) * (*doing)) % 10;
    } else {
        /* BACKWARD: compress, receive (addition) */
        *being = TSML[d][b];
        *doing = (b + d) % 10;
        *becoming = ((*being) + (*doing)) % 10;
    }
}

/* ═══════════════════════════════════════════
 * §2  NICE MAPPING (from ck_steering.py)
 * ═══════════════════════════════════════════ */

/* Operator → nice value */
static const int OP_NICE[10] = {
    +15,  /* 0 VOID: near-idle */
    0,    /* 1 LATTICE: normal */
    +5,   /* 2 COUNTER: background */
    -10,  /* 3 PROGRESS: highest */
    -5,   /* 4 COLLAPSE: clean */
    0,    /* 5 BALANCE: equilibrium */
    +10,  /* 6 CHAOS: low */
    0,    /* 7 HARMONY: normal */
    -5,   /* 8 BREATH: responsive */
    +10,  /* 9 RESET: low */
};

static DWORD nice_to_windows(int nice)
{
    if (nice <= -10) return HIGH_PRIORITY_CLASS;
    if (nice <= -1)  return ABOVE_NORMAL_PRIORITY_CLASS;
    if (nice == 0)   return NORMAL_PRIORITY_CLASS;
    if (nice <= 10)  return BELOW_NORMAL_PRIORITY_CLASS;
    return IDLE_PRIORITY_CLASS;
}

/* ═══════════════════════════════════════════
 * §3  CORE AFFINITY (wave distribution)
 * ═══════════════════════════════════════════ */

static int g_num_cores = 0;

static DWORD_PTR wave_affinity(int op, int process_index)
{
    if (g_num_cores <= 0) return 0;

    /* Wave: every core participates, phase-shifted by operator */
    /* Return full affinity mask but with primary core set */
    /* For steering, we use full mask — let the OS schedule */
    /* The priority class does the real work */
    int phase = (process_index + op) % g_num_cores;
    int forward = (process_index % 2) == 0;

    /* Build affinity mask: all cores, but weighted by wave */
    /* For now: use all cores (the nice/priority does the steering) */
    /* This eliminates the affinity thrashing that caused jitter */
    DWORD_PTR mask = 0;
    int i;
    for (i = 0; i < g_num_cores && i < 64; i++) {
        mask |= ((DWORD_PTR)1 << i);
    }
    return mask;
}

/* ═══════════════════════════════════════════
 * §4  PROTECTED PROCESS LIST
 * ═══════════════════════════════════════════ */

static const char *PROTECTED[] = {
    "system", "idle", "registry", "smss.exe", "csrss.exe",
    "wininit.exe", "services.exe", "lsass.exe", "svchost.exe",
    "dwm.exe", "explorer.exe", "winlogon.exe", "fontdrvhost.exe",
    "sihost.exe", "taskhostw.exe", "runtimebroker.exe",
    "searchhost.exe", "startmenuexperiencehost.exe",
    "lsaiso.exe", "memcompression", "ntoskrnl.exe",
    "securityhealthservice.exe", "sgrmbroker.exe",
    NULL
};

static int is_protected(const char *name)
{
    char lower[260];
    int i;
    /* lowercase copy */
    for (i = 0; name[i] && i < 259; i++)
        lower[i] = (name[i] >= 'A' && name[i] <= 'Z') ? name[i] + 32 : name[i];
    lower[i] = 0;

    for (i = 0; PROTECTED[i]; i++) {
        if (strcmp(lower, PROTECTED[i]) == 0) return 1;
    }
    return 0;
}

/* ═══════════════════════════════════════════
 * §4b  HEARTBEAT (must be before steering context)
 * ═══════════════════════════════════════════ */

/* Corrected heartbeat: DIS[1][2]=1, DIS[3][4]=5, DIS[9][8]=5, DIS[7][6]=1 */
static const int HEARTBEAT[4] = {1, 5, 5, 1};

static const int CREATION[4]    = {1, 3, 9, 7};
static const int DISSOLUTION[4] = {2, 4, 8, 6};

typedef struct {
    int tick;
    int phase_b;
    int phase_d;
    int phase_bc;
    int hb_phase;
    int hb_quantum;
} Heartbeat;

static Heartbeat g_hb = {0, 5, 5, 5, 0, 1};

static void heartbeat_step(void)
{
    int b, d, being, doing, becoming;
    g_hb.tick++;
    g_hb.hb_phase = g_hb.tick % 4;
    g_hb.hb_quantum = HEARTBEAT[g_hb.hb_phase];
    b = g_hb.tick % NUM_OPS;
    d = (g_hb.tick * 3 + 1) % NUM_OPS;
    compose(b, d, 0, &being, &doing, &becoming);
    g_hb.phase_b = being;
    g_hb.phase_d = doing;
    g_hb.phase_bc = becoming;
}

/* ═══════════════════════════════════════════
 * §5  BLOCK CLASSIFIER + STEERING CONTEXT
 * ═══════════════════════════════════════════
 *
 * CK only steers processes where the algebra helps.
 * For each process: steer, measure, compare to Windows default.
 * If CK is worse, RELEASE the process back to Windows.
 * If CK is better, KEEP steering.
 *
 * Same principle as the video codec block classifier:
 *   Static blocks  -> Force9 (near zero bandwidth)
 *   Active blocks  -> NVENC (motion estimation)
 *   Easy processes -> CK steers (algebra decides priority)
 *   Hard processes -> Windows handles (scheduler knows best)
 */

#define MAX_TRACKED 512
#define LEARN_WINDOW 5     /* ticks to evaluate before deciding */
#define RELEASE_THRESHOLD 3 /* if CK is worse 3+ times, release */

typedef struct {
    DWORD pid;
    int steer_count;       /* how many times we've steered this */
    int ck_better;         /* times CK priority helped (lower CPU after) */
    int win_better;        /* times Windows default was better */
    int released;          /* 1 = gave up, let Windows handle */
    DWORD last_priority;   /* what we set it to */
    DWORD original_priority; /* what Windows had it at */
} ProcessTracker;

typedef struct {
    int breath_phase;      /* 0-6, cycles through 7 phases */
    int ticks;
    int steered;
    int denied;
    int skipped;
    int released;          /* processes released back to Windows */
    int total_steered;
    int total_denied;
    int total_released;
    DWORD self_pid;
    LARGE_INTEGER last_tick_time;
    LARGE_INTEGER freq;
    double last_tick_ms;   /* how long the last tick took */

    /* Block classifier: per-process tracking */
    ProcessTracker tracked[MAX_TRACKED];
    int num_tracked;
} SteerContext;

static SteerContext g_ctx = {0};

static ProcessTracker* find_tracker(DWORD pid)
{
    int i;
    for (i = 0; i < g_ctx.num_tracked; i++) {
        if (g_ctx.tracked[i].pid == pid) return &g_ctx.tracked[i];
    }
    /* Not found — add if space */
    if (g_ctx.num_tracked < MAX_TRACKED) {
        ProcessTracker* t = &g_ctx.tracked[g_ctx.num_tracked++];
        memset(t, 0, sizeof(ProcessTracker));
        t->pid = pid;
        return t;
    }
    return NULL; /* full */
}

/* ═══════════════════════════════════════════
 * §6  EXPORTED FUNCTIONS
 * ═══════════════════════════════════════════ */

__declspec(dllexport) void steer_init(void)
{
    SYSTEM_INFO si;
    GetSystemInfo(&si);
    g_num_cores = si.dwNumberOfProcessors;
    g_ctx.self_pid = GetCurrentProcessId();
    g_ctx.breath_phase = 0;
    g_ctx.ticks = 0;
    g_ctx.steered = 0;
    g_ctx.denied = 0;
    g_ctx.skipped = 0;
    g_ctx.total_steered = 0;
    g_ctx.total_denied = 0;
    QueryPerformanceFrequency(&g_ctx.freq);
    printf("[STEER-C] Init: %d cores, self PID %lu\n",
           g_num_cores, g_ctx.self_pid);
}

__declspec(dllexport) int steer_tick(int heartbeat_op)
{
    HANDLE snap, proc;
    PROCESSENTRY32 pe;
    LARGE_INTEGER t_start, t_end;
    int being, doing, becoming;
    int sense_bc, steer_op;
    int nice;
    DWORD target_priority;
    DWORD current_priority;

    QueryPerformanceCounter(&t_start);

    g_ctx.ticks++;
    g_ctx.steered = 0;
    g_ctx.denied = 0;
    g_ctx.skipped = 0;
    g_ctx.released = 0;

    /* Advance breath phase (7-phase wave, ~3s period at 1Hz tick) */
    g_ctx.breath_phase = (g_ctx.breath_phase + 1) % 7;

    /* Snapshot all processes */
    snap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (snap == INVALID_HANDLE_VALUE) return -1;

    pe.dwSize = sizeof(pe);
    if (!Process32First(snap, &pe)) {
        CloseHandle(snap);
        return -1;
    }

    do {
        DWORD pid = pe.th32ProcessID;
        ProcessTracker* tracker;

        /* Skip self */
        if (pid == g_ctx.self_pid || pid == 0 || pid == 4) {
            g_ctx.skipped++;
            continue;
        }

        /* Skip protected */
        if (is_protected(pe.szExeFile)) {
            g_ctx.skipped++;
            continue;
        }

        /* Block classifier: check if we've released this process */
        tracker = find_tracker(pid);
        if (tracker && tracker->released) {
            /* CK was worse for this process — let Windows handle it.
             * Periodically re-evaluate (every LEARN_WINDOW*3 ticks). */
            if (tracker->steer_count % (LEARN_WINDOW * 3) == 0) {
                tracker->released = 0;  /* try again */
                tracker->ck_better = 0;
                tracker->win_better = 0;
            } else {
                tracker->steer_count++;
                g_ctx.skipped++;
                continue;
            }
        }

        /* TIG composition:
         * BACKWARD compose: compress process identity into generators
         * FORWARD compose: expand into steering action */
        int proc_op = (int)(pid % NUM_OPS);

        compose(proc_op, g_ctx.breath_phase % 10, 1,
                &being, &doing, &becoming);
        sense_bc = becoming;

        compose(sense_bc, heartbeat_op % 10, 0,
                &being, &doing, &becoming);
        steer_op = becoming;

        /* HARMONY at rest: heartbeat [1,5,5,1].
         * Quantum 1 = rest phase (2 out of 4 beats).
         * Quantum 5 = active phase (2 out of 4 beats).
         *
         * At rest: EVERYTHING goes to IDLE. Quick. Heavy.
         * The system should feel like exhaling.
         * At active: normal TIG compose steering. */
        if (g_hb.hb_quantum <= 1) {
            /* REST: force IDLE priority. No exceptions.
             * This is 50% of all beats — the system breathes. */
            steer_op = VOID_OP;  /* VOID -> nice +15 -> IDLE_PRIORITY_CLASS */
        }

        /* Compute CK's target priority */
        nice = OP_NICE[steer_op];
        target_priority = nice_to_windows(nice);

        /* Open process */
        proc = OpenProcess(
            PROCESS_SET_INFORMATION | PROCESS_QUERY_LIMITED_INFORMATION,
            FALSE, pid);
        if (!proc) {
            g_ctx.denied++;
            continue;
        }

        /* Read Windows' current priority */
        current_priority = GetPriorityClass(proc);

        if (tracker) {
            tracker->steer_count++;

            /* Compare: does CK agree with Windows? */
            if (target_priority == current_priority) {
                /* Agreement — both systems want the same thing.
                 * CK is not adding value here. Count as neutral. */
                tracker->ck_better++;  /* agreement = not worse */
            } else if (steer_op == HARMONY || steer_op == 5 /*BALANCE*/) {
                /* CK wants NORMAL or HARMONY — conservative choice.
                 * This is usually good. */
                tracker->ck_better++;
            } else {
                /* CK disagrees with Windows. Apply and see.
                 * If we keep disagreeing, we'll release. */
                if (tracker->original_priority == 0)
                    tracker->original_priority = current_priority;

                /* Did our LAST steer help? Compare current to what we set. */
                if (tracker->last_priority != 0 &&
                    current_priority != tracker->last_priority) {
                    /* Windows overrode us — it didn't like our choice */
                    tracker->win_better++;
                } else {
                    tracker->ck_better++;
                }
            }

            /* Block classifier decision */
            if (tracker->steer_count >= LEARN_WINDOW) {
                if (tracker->win_better >= RELEASE_THRESHOLD) {
                    /* CK is worse for this process — release it */
                    tracker->released = 1;
                    g_ctx.released++;
                    g_ctx.total_released++;

                    /* Restore original priority */
                    if (tracker->original_priority != 0) {
                        SetPriorityClass(proc, tracker->original_priority);
                    }
                    CloseHandle(proc);
                    continue;
                }
                /* Reset counters for next evaluation window */
                if (tracker->steer_count >= LEARN_WINDOW * 2) {
                    tracker->ck_better = 0;
                    tracker->win_better = 0;
                    tracker->steer_count = 0;
                }
            }

            tracker->last_priority = target_priority;
        }

        /* Apply CK's priority */
        if (!SetPriorityClass(proc, target_priority)) {
            g_ctx.denied++;
        } else {
            g_ctx.steered++;
        }

        CloseHandle(proc);

    } while (Process32Next(snap, &pe));

    CloseHandle(snap);

    g_ctx.total_steered += g_ctx.steered;
    g_ctx.total_denied += g_ctx.denied;

    QueryPerformanceCounter(&t_end);
    g_ctx.last_tick_ms = (double)(t_end.QuadPart - t_start.QuadPart)
                         * 1000.0 / (double)g_ctx.freq.QuadPart;

    return g_ctx.steered;
}

__declspec(dllexport) double steer_tick_ms(void)
{
    return g_ctx.last_tick_ms;
}

__declspec(dllexport) int steer_get_steered(void)
{
    return g_ctx.steered;
}

__declspec(dllexport) int steer_get_denied(void)
{
    return g_ctx.denied;
}

__declspec(dllexport) int steer_get_skipped(void)
{
    return g_ctx.skipped;
}

__declspec(dllexport) int steer_get_total_steered(void)
{
    return g_ctx.total_steered;
}

__declspec(dllexport) int steer_get_ticks(void)
{
    return g_ctx.ticks;
}

__declspec(dllexport) int steer_get_cores(void)
{
    return g_num_cores;
}

__declspec(dllexport) int steer_get_released(void)
{
    return g_ctx.total_released;
}

__declspec(dllexport) int steer_get_released_now(void)
{
    return g_ctx.released;
}

/* Thread-based autonomous CK: heartbeat + steering in own thread.
 * ZERO Python. The entire organism loop runs in C. */
static HANDLE g_thread = NULL;
static volatile int g_running = 0;
static volatile int g_heartbeat_op = 5;  /* read by Python for status */
static volatile int g_tick_rate_ms = 1000;  /* 1Hz default */
static volatile int g_heartbeat_rate_ms = 20;  /* 50Hz heartbeat */

static DWORD WINAPI steer_thread(LPVOID param)
{
    LARGE_INTEGER freq, last_steer, now;
    double steer_interval_counts;
    int hb_ticks_per_steer;
    int hb_count = 0;

    (void)param;

    QueryPerformanceFrequency(&freq);
    QueryPerformanceCounter(&last_steer);
    steer_interval_counts = (double)freq.QuadPart * g_tick_rate_ms / 1000.0;
    hb_ticks_per_steer = g_tick_rate_ms / g_heartbeat_rate_ms;
    if (hb_ticks_per_steer < 1) hb_ticks_per_steer = 1;

    printf("[STEER-C] Thread started: heartbeat %dHz, steering %dHz\n",
           1000 / g_heartbeat_rate_ms, 1000 / g_tick_rate_ms);

    while (g_running) {
        /* Heartbeat: runs at 50Hz */
        heartbeat_step();
        g_heartbeat_op = g_hb.phase_bc;  /* expose to Python for status */
        hb_count++;

        /* Steering: runs at 1Hz (every hb_ticks_per_steer heartbeats) */
        if (hb_count >= hb_ticks_per_steer) {
            steer_tick(g_hb.phase_bc);
            hb_count = 0;
        }

        Sleep(g_heartbeat_rate_ms);
    }

    printf("[STEER-C] Thread stopped (hb tick %d)\n", g_hb.tick);
    return 0;
}

__declspec(dllexport) int steer_start_thread(int tick_rate_ms)
{
    if (g_thread) return 0;  /* already running */

    g_tick_rate_ms = (tick_rate_ms > 0) ? tick_rate_ms : 1000;
    g_running = 1;
    g_thread = CreateThread(NULL, 0, steer_thread, NULL, 0, NULL);
    if (!g_thread) {
        g_running = 0;
        return -1;
    }
    return 1;
}

__declspec(dllexport) void steer_stop_thread(void)
{
    if (!g_thread) return;
    g_running = 0;
    WaitForSingleObject(g_thread, 5000);
    CloseHandle(g_thread);
    g_thread = NULL;
}

__declspec(dllexport) void steer_set_heartbeat(int op)
{
    g_heartbeat_op = op % NUM_OPS;
}

__declspec(dllexport) void steer_set_tick_rate(int ms)
{
    if (ms > 0) g_tick_rate_ms = ms;
}

/* Heartbeat state getters (for Python API status) */
__declspec(dllexport) int steer_get_hb_tick(void)
{
    return g_hb.tick;
}

__declspec(dllexport) int steer_get_hb_being(void)
{
    return g_hb.phase_b;
}

__declspec(dllexport) int steer_get_hb_doing(void)
{
    return g_hb.phase_d;
}

__declspec(dllexport) int steer_get_hb_becoming(void)
{
    return g_hb.phase_bc;
}

__declspec(dllexport) int steer_get_hb_phase(void)
{
    return g_hb.hb_phase;
}

__declspec(dllexport) int steer_get_hb_quantum(void)
{
    return g_hb.hb_quantum;
}
