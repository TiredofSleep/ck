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
 * §5  STEERING CONTEXT
 * ═══════════════════════════════════════════ */

typedef struct {
    int breath_phase;      /* 0-6, cycles through 7 phases */
    int ticks;
    int steered;
    int denied;
    int skipped;
    int total_steered;
    int total_denied;
    DWORD self_pid;
    LARGE_INTEGER last_tick_time;
    LARGE_INTEGER freq;
    double last_tick_ms;   /* how long the last tick took */
} SteerContext;

static SteerContext g_ctx = {0};

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

    QueryPerformanceCounter(&t_start);

    g_ctx.ticks++;
    g_ctx.steered = 0;
    g_ctx.denied = 0;
    g_ctx.skipped = 0;

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

        /* Compute priority */
        nice = OP_NICE[steer_op];
        target_priority = nice_to_windows(nice);

        /* Open process with limited rights */
        proc = OpenProcess(
            PROCESS_SET_INFORMATION | PROCESS_QUERY_LIMITED_INFORMATION,
            FALSE, pid);
        if (!proc) {
            g_ctx.denied++;
            continue;
        }

        /* Set priority class */
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

/* Thread-based autonomous steering: runs in its own thread, no Python GIL */
static HANDLE g_thread = NULL;
static volatile int g_running = 0;
static volatile int g_heartbeat_op = 5;  /* BALANCE default */
static volatile int g_tick_rate_ms = 1000;  /* 1Hz default */

static DWORD WINAPI steer_thread(LPVOID param)
{
    (void)param;
    printf("[STEER-C] Thread started: tick rate %d ms\n", g_tick_rate_ms);

    while (g_running) {
        steer_tick(g_heartbeat_op);
        Sleep(g_tick_rate_ms);
    }

    printf("[STEER-C] Thread stopped\n");
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
