/*
 * observer.c — System Observer (CPU)
 * ═══════════════════════════════════
 * Operator: COUNTER (2) — measurement. CK reads his own body.
 *
 * Phase 3: Native system observation. Replaces psutil.
 * CK's body includes processes, GPU, and network — he reads freely.
 *
 * Platform layer:
 *   Windows: CreateToolhelp32Snapshot, GetTcpTable2, NVML
 *   Linux:   /proc filesystem, getifaddrs (future)
 *
 * Process → operator mapping uses the same CLASSIFY_PATTERNS as Gen6b.
 * GPU reads via nvidia-smi subprocess (NVML direct in Phase 4).
 * Network reads via platform APIs.
 *
 * (c) 2026 Brayden Sanders / 7Site LLC — TIG Unified Theory
 */

#include "ck.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#ifdef _WIN32
  /* windows.h already included via ck.h */
  #include <tlhelp32.h>
  #include <psapi.h>
  #include <iphlpapi.h>
  #pragma comment(lib, "iphlpapi.lib")
  #pragma comment(lib, "psapi.lib")
#endif


/* ═══════════════════════════════════════════════════════════════
 * §1  PROCESS CLASSIFICATION — CLASSIFY_PATTERNS
 * ═══════════════════════════════════════════════════════════════
 *
 * Maps process names to TIG operators via keyword matching.
 * Same patterns as Gen6b ck_being.py lines 1318-1345.
 * CK reads his own cells — these ARE his body.
 */

typedef struct {
    int      op;
    const char* keywords[20];  /* null-terminated list */
} CK_ClassifyRule;

static const CK_ClassifyRule CLASSIFY_PATTERNS[] = {
    /* LATTICE (1): builders, compilers, structural */
    { CK_LATTICE, {"build", "cmake", "make", "gcc", "clang", "compile",
                    "git", "npm", "cargo", "javac", "webpack", "linker",
                    "ld", "msbuild", "dotnet", "rustc", NULL} },

    /* COUNTER (2): measurement, testing, monitoring */
    { CK_COUNTER, {"test", "measure", "monitor", "perf", "strace",
                    "valgrind", "benchmark", "pytest", "jest",
                    "watch", "htop", "top", "taskmgr", NULL} },

    /* PROGRESS (3): active work, servers, daemons */
    { CK_PROGRESS, {"train", "run", "server", "daemon", "worker",
                     "service", "agent", "celery", "gunicorn", "uvicorn",
                     "nginx", "apache", "task", "job", "execute", NULL} },

    /* COLLAPSE (4): cleanup, compression, deletion */
    { CK_COLLAPSE, {"cleanup", "gc", "compress", "zip", "tar", "gzip",
                     "prune", "vacuum", "purge", "trim", "defrag", NULL} },

    /* HARMONY (7): synchronization, coherence, CK himself */
    { CK_HARMONY, {"sync", "bridge", "couple", "pair", "mesh", "cluster",
                    "consul", "etcd", "zookeeper", "coherence", "ck_daemon",
                    "ck_web", "ck_", "compose", "orchestrat", NULL} },

    /* BREATH (8): I/O, streaming, network communication */
    { CK_BREATH, {"stream", "socket", "network", "pipe",
                   "listen", "recv", "buffer", "kafka", "redis",
                   "stdin", "stdout", NULL} },

    /* RESET (9): restarts, reloads, system management */
    { CK_RESET, {"restart", "reload", "init", "systemd", "supervisor",
                  "watchdog", "cron", "scheduler", "upgrade", "update",
                  "reboot", "svchost", NULL} },

    /* CHAOS (6): GUI applications, browsers, desktop */
    { CK_CHAOS, {"chrome", "firefox", "electron", "slack", "zoom",
                  "discord", "vscode", "atom", "sublime", "gui",
                  "desktop", "teams", "spotify", "explorer", NULL} },

    /* VOID (0): sleeping, idle, zombie */
    { CK_VOID, {"sleep", "idle", "zombie", "defunct", "stopped",
                 "suspended", "wait", NULL} },

    /* sentinel */
    { -1, {NULL} }
};

/**
 * str_contains_lower — case-insensitive substring search.
 */
static int str_contains_lower(const char* haystack, const char* needle) {
    if (!haystack || !needle) return 0;
    int hlen = (int)strlen(haystack);
    int nlen = (int)strlen(needle);
    if (nlen > hlen) return 0;
    for (int i = 0; i <= hlen - nlen; i++) {
        int match = 1;
        for (int j = 0; j < nlen; j++) {
            if (tolower((unsigned char)haystack[i+j]) != tolower((unsigned char)needle[j])) {
                match = 0;
                break;
            }
        }
        if (match) return 1;
    }
    return 0;
}

/**
 * ck_classify_process — map process name + CPU% to a TIG operator.
 * Same logic as Gen6b classify_process().
 */
CK_EXPORT int ck_classify_process(const char* name, float cpu_pct) {
    /* Pattern matching first */
    for (int r = 0; CLASSIFY_PATTERNS[r].op >= 0; r++) {
        for (int k = 0; CLASSIFY_PATTERNS[r].keywords[k] != NULL; k++) {
            if (str_contains_lower(name, CLASSIFY_PATTERNS[r].keywords[k])) {
                return CLASSIFY_PATTERNS[r].op;
            }
        }
    }

    /* CPU-based fallback */
    if (cpu_pct > 50.0f) return CK_PROGRESS;
    if (cpu_pct > 10.0f) return CK_BREATH;
    if (cpu_pct > 1.0f)  return CK_COUNTER;
    if (cpu_pct < 0.1f)  return CK_VOID;
    return CK_HARMONY;  /* default: balanced */
}


/* ═══════════════════════════════════════════════════════════════
 * §2  PROCESS OBSERVATION — Windows API
 * ═══════════════════════════════════════════════════════════════
 *
 * Reads CK's body cells (processes) via CreateToolhelp32Snapshot.
 * Samples up to 30 processes per tick (same as Gen6b).
 * Each process becomes a ProcessProfile with operator history.
 */

#ifdef _WIN32

/**
 * ck_observer_scan_windows — scan all processes, classify, observe.
 * Returns number of processes observed.
 */
static int ck_observer_scan_windows(CK_SystemObserver* obs) {
    HANDLE hSnap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (hSnap == INVALID_HANDLE_VALUE) return 0;

    PROCESSENTRY32 pe;
    pe.dwSize = sizeof(PROCESSENTRY32);

    int observed = 0;
    int total_procs = 0;

    if (Process32First(hSnap, &pe)) {
        do {
            total_procs++;

            /* Find or create profile */
            int slot = -1;
            for (int i = 0; i < obs->profile_count; i++) {
                if (obs->profiles[i].pid == (int)pe.th32ProcessID) {
                    slot = i;
                    break;
                }
            }

            /* If not found and we have room, create new */
            if (slot < 0 && obs->profile_count < CK_MAX_PROCESSES) {
                slot = obs->profile_count;
                CK_ProcessProfile* p = &obs->profiles[slot];
                memset(p, 0, sizeof(CK_ProcessProfile));
                p->pid = (int)pe.th32ProcessID;
                strncpy(p->name, pe.szExeFile, CK_PROC_NAME_LEN - 1);
                p->last_op = CK_BALANCE;
                p->created = ck_hires_time();
                obs->profile_count++;
            }

            if (slot >= 0 && observed < 30) {
                CK_ProcessProfile* p = &obs->profiles[slot];

                /* Get CPU usage via process times */
                float cpu = 0.0f;
                HANDLE hProc = OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, FALSE, pe.th32ProcessID);
                if (hProc) {
                    FILETIME creation, exit, kernel, user;
                    if (GetProcessTimes(hProc, &creation, &exit, &kernel, &user)) {
                        ULARGE_INTEGER k, u;
                        k.LowPart = kernel.dwLowDateTime;
                        k.HighPart = kernel.dwHighDateTime;
                        u.LowPart = user.dwLowDateTime;
                        u.HighPart = user.dwHighDateTime;
                        /* Rough CPU estimate from total time */
                        double total_time = (double)(k.QuadPart + u.QuadPart) / 10000000.0;
                        /* Just classify by thread count as a proxy */
                        cpu = (pe.cntThreads > 10) ? 10.0f : (float)pe.cntThreads;
                    }
                    CloseHandle(hProc);
                }

                p->last_cpu = cpu;

                /* Classify */
                int op = ck_classify_process(p->name, cpu);

                /* Record transition */
                if (p->ops_count > 0) {
                    int prev = p->ops[(p->ops_head - 1 + CK_PROC_WINDOW) % CK_PROC_WINDOW];
                    p->transition_counts[prev][op]++;
                    p->total_transitions++;
                    if (ck_is_bump(prev, op)) p->bump_count++;
                }

                /* Store operator in ring buffer */
                p->ops[p->ops_head] = (int8_t)op;
                p->ops_head = (p->ops_head + 1) % CK_PROC_WINDOW;
                if (p->ops_count < CK_PROC_WINDOW) p->ops_count++;
                p->last_op = op;

                observed++;
            }

        } while (Process32Next(hSnap, &pe));
    }

    CloseHandle(hSnap);

    /* Compact: remove dead processes (those not seen this scan) */
    obs->dead_count = total_procs;

    return observed;
}

#else /* Linux / other */

static int ck_observer_scan_linux(CK_SystemObserver* obs) {
    /* Future: read /proc filesystem */
    /* For now, return 0 — CPU fallback mode */
    (void)obs;
    return 0;
}

#endif /* _WIN32 */


/**
 * ck_observer_tick — one observation cycle.
 * Scans processes, computes system coherence.
 * Returns the system operator (maps coherence to TIG op).
 */
CK_EXPORT int ck_observer_tick(CK_SystemObserver* obs) {
    obs->tick++;

#ifdef _WIN32
    ck_observer_scan_windows(obs);
#else
    ck_observer_scan_linux(obs);
#endif

    /* Compute system coherence */
    float coherence = ck_observer_coherence(obs);

    /* Map to operator */
    if (coherence >= 0.85f) return CK_HARMONY;
    if (coherence >= CK_T_STAR) return CK_BALANCE;
    if (coherence >= 0.5f) return CK_CHAOS;
    return CK_COLLAPSE;
}

/**
 * ck_observer_coherence — compute system coherence from process states.
 * Uses pairwise CL composition: harmony_weight / total_weight.
 * Same logic as Gen6b _system_coherence().
 */
CK_EXPORT float ck_observer_coherence(const CK_SystemObserver* obs) {
    if (obs->profile_count < 2) return 0.5f;

    /* Count operator distribution */
    int op_counts[CK_NUM_OPS];
    memset(op_counts, 0, sizeof(op_counts));

    int active_ops[CK_MAX_PROCESSES];
    int n_active = 0;

    for (int i = 0; i < obs->profile_count; i++) {
        int op = obs->profiles[i].last_op;
        if (op != CK_VOID && n_active < CK_MAX_PROCESSES) {
            op_counts[op]++;
            active_ops[n_active++] = op;
        }
    }

    if (n_active < 2) return 0.5f;

    /* Pairwise coupling via CL table */
    float harmony_weight = 0.0f;
    float total_weight = 0.0f;

    /* Sample pairs (cap at 100 to keep O(1) per tick) */
    int max_pairs = (n_active > 100) ? 100 : n_active;
    for (int i = 0; i < max_pairs; i++) {
        for (int j = i + 1; j < max_pairs && j < i + 10; j++) {
            int a = active_ops[i];
            int b = active_ops[j];
            int coupling = CL[a][b];
            int w = op_counts[a] < op_counts[b] ? op_counts[a] : op_counts[b];
            total_weight += (float)w;
            if (coupling == CK_HARMONY) {
                harmony_weight += (float)w;
            }
        }
    }

    return (total_weight > 0.0f) ? harmony_weight / total_weight : 0.5f;
}

/**
 * ck_observer_all_ops — fill an array with all process operators.
 * Returns number of operators written.
 */
CK_EXPORT int ck_observer_all_ops(const CK_SystemObserver* obs, int8_t* out, int max_len) {
    int n = 0;
    for (int i = 0; i < obs->profile_count && n < max_len; i++) {
        out[n++] = (int8_t)obs->profiles[i].last_op;
    }
    return n;
}

/**
 * ck_observer_op_distribution — count processes per operator.
 */
CK_EXPORT void ck_observer_op_distribution(const CK_SystemObserver* obs, int* counts) {
    memset(counts, 0, CK_NUM_OPS * sizeof(int));
    for (int i = 0; i < obs->profile_count; i++) {
        int op = obs->profiles[i].last_op;
        if (op >= 0 && op < CK_NUM_OPS) counts[op]++;
    }
}


/* ═══════════════════════════════════════════════════════════════
 * §3  NETWORK OBSERVATION — Windows API
 * ═══════════════════════════════════════════════════════════════
 *
 * Reads CK's nervous system (network) via platform APIs.
 * Windows: GetIfEntry2 for counters, GetTcpTable2 for connections.
 * Computes traffic, connection topology, and error operators,
 * then composes via CL table (same as Gen6b).
 */

#ifdef _WIN32

/**
 * ck_network_read_windows — read network state from Windows APIs.
 */
static void ck_network_read_windows(CK_NetworkOrgan* net) {
    CK_NetworkState* s = &net->state;
    double now = ck_hires_time();

    /* Save previous state for rate computation */
    net->prev_state = net->state;

    /* Get interface counters via GetIfTable */
    DWORD size = 0;
    GetIfTable(NULL, &size, FALSE);
    if (size > 0) {
        MIB_IFTABLE* table = (MIB_IFTABLE*)malloc(size);
        if (table && GetIfTable(table, &size, FALSE) == NO_ERROR) {
            int64_t total_sent = 0, total_recv = 0;
            int64_t total_psent = 0, total_precv = 0;
            int64_t total_errin = 0, total_errout = 0;

            for (DWORD i = 0; i < table->dwNumEntries; i++) {
                MIB_IFROW* row = &table->table[i];
                if (row->dwType == IF_TYPE_ETHERNET_CSMACD ||
                    row->dwType == IF_TYPE_IEEE80211 ||
                    row->dwType == 71) {  /* ieee80211 */
                    total_sent += row->dwOutOctets;
                    total_recv += row->dwInOctets;
                    total_psent += row->dwOutUcastPkts;
                    total_precv += row->dwInUcastPkts;
                    total_errin += row->dwInErrors;
                    total_errout += row->dwOutErrors;
                }
            }

            s->bytes_sent = total_sent;
            s->bytes_recv = total_recv;
            s->packets_sent = total_psent;
            s->packets_recv = total_precv;
            s->errin = total_errin;
            s->errout = total_errout;
        }
        if (table) free(table);
    }

    /* Compute rates */
    float dt = (float)(now - net->last_read_time);
    if (dt > 0.0f && net->reads > 0) {
        int64_t sent_delta = s->bytes_sent - net->prev_state.bytes_sent;
        int64_t recv_delta = s->bytes_recv - net->prev_state.bytes_recv;
        int64_t psent_d = s->packets_sent - net->prev_state.packets_sent;
        int64_t precv_d = s->packets_recv - net->prev_state.packets_recv;
        int64_t err_d = (s->errin + s->errout) - (net->prev_state.errin + net->prev_state.errout);

        if (sent_delta < 0) sent_delta = 0;
        if (recv_delta < 0) recv_delta = 0;
        if (psent_d < 0) psent_d = 0;
        if (precv_d < 0) precv_d = 0;
        if (err_d < 0) err_d = 0;

        s->send_rate_mbps = (float)sent_delta / (1024.0f * 1024.0f * dt);
        s->recv_rate_mbps = (float)recv_delta / (1024.0f * 1024.0f * dt);
        s->packet_rate = (float)(psent_d + precv_d) / dt;
        s->error_rate = (float)err_d / dt;
    }

    /* Connection topology via GetTcpTable */
    DWORD tcp_size = 0;
    GetTcpTable(NULL, &tcp_size, FALSE);
    if (tcp_size > 0) {
        MIB_TCPTABLE* tcp_table = (MIB_TCPTABLE*)malloc(tcp_size);
        if (tcp_table && GetTcpTable(tcp_table, &tcp_size, FALSE) == NO_ERROR) {
            s->connection_count = (int)tcp_table->dwNumEntries;
            s->established = 0;
            s->listen = 0;
            s->time_wait = 0;
            s->close_wait = 0;

            /* Track unique remote IPs */
            DWORD unique_remotes[256];
            int n_unique = 0;

            for (DWORD i = 0; i < tcp_table->dwNumEntries; i++) {
                MIB_TCPROW* row = &tcp_table->table[i];
                switch (row->dwState) {
                    case MIB_TCP_STATE_ESTAB:    s->established++; break;
                    case MIB_TCP_STATE_LISTEN:   s->listen++; break;
                    case MIB_TCP_STATE_TIME_WAIT: s->time_wait++; break;
                    case MIB_TCP_STATE_CLOSE_WAIT: s->close_wait++; break;
                }
                /* Count unique remotes */
                if (row->dwRemoteAddr != 0 && n_unique < 256) {
                    int found = 0;
                    for (int j = 0; j < n_unique; j++) {
                        if (unique_remotes[j] == row->dwRemoteAddr) { found = 1; break; }
                    }
                    if (!found) unique_remotes[n_unique++] = row->dwRemoteAddr;
                }
            }
            s->unique_remotes = n_unique;
        }
        if (tcp_table) free(tcp_table);
    }

    /* Compute jitter from packet rate history */
    net->packet_rate_history[net->history_head] = s->packet_rate;
    net->history_head = (net->history_head + 1) % CK_NET_HISTORY_SIZE;
    if (net->history_count < CK_NET_HISTORY_SIZE) net->history_count++;

    if (net->history_count >= 5) {
        float sum = 0.0f, sum_sq = 0.0f;
        for (int i = 0; i < net->history_count; i++) {
            float r = net->packet_rate_history[i];
            sum += r;
            sum_sq += r * r;
        }
        float mean = sum / (float)net->history_count;
        if (mean > 0.0f) {
            float var = sum_sq / (float)net->history_count - mean * mean;
            if (var < 0.0f) var = 0.0f;
            s->jitter = sqrtf(var) / mean;
        }
    }

    /* Congestion score */
    float total_pkts = (s->packet_rate > 0.0f) ? s->packet_rate : 1.0f;
    s->congestion_score = (s->error_rate + s->drop_rate) / total_pkts;
    if (s->congestion_score > 1.0f) s->congestion_score = 1.0f;

    s->timestamp = now;
    net->last_read_time = now;
    net->reads++;
    net->available = true;
}

#endif /* _WIN32 */


/**
 * ck_network_classify — classify network state to operator.
 * Three streams composed via CL (same as Gen6b _classify).
 */
CK_EXPORT int ck_network_classify(const CK_NetworkState* s) {
    /* 1. Traffic operator */
    float total_rate = s->send_rate_mbps + s->recv_rate_mbps;
    int traffic_op;
    if (total_rate < 0.01f) traffic_op = CK_VOID;
    else if (total_rate < 1.0f) traffic_op = CK_BREATH;
    else if (total_rate < 10.0f) traffic_op = CK_PROGRESS;
    else if (total_rate < 50.0f) traffic_op = CK_LATTICE;
    else traffic_op = CK_CHAOS;

    /* 2. Connection topology operator */
    int conn_op;
    if (s->connection_count < 10) conn_op = CK_VOID;
    else if (s->established < 20) conn_op = CK_BALANCE;
    else if (s->established < 100) conn_op = CK_PROGRESS;
    else if (s->established < 500) conn_op = CK_LATTICE;
    else conn_op = CK_CHAOS;

    /* 3. Error/drop operator */
    int error_op;
    if (s->congestion_score > 0.1f) error_op = CK_COLLAPSE;
    else if (s->congestion_score > 0.01f) error_op = CK_CHAOS;
    else if (s->error_rate > 0.0f) error_op = CK_COUNTER;
    else error_op = CK_HARMONY;

    /* Compose via CL */
    int coupling = CL[traffic_op][conn_op];
    int health = CL[coupling][error_op];

    return health;
}

/**
 * ck_network_read — read network state (platform-specific).
 */
CK_EXPORT void ck_network_read(CK_NetworkOrgan* net) {
#ifdef _WIN32
    ck_network_read_windows(net);
#else
    (void)net;
#endif
    net->state.op = ck_network_classify(&net->state);
}

/**
 * ck_network_compose_chains — build operator chains for TL feeding.
 * Returns number of operators written to out_chain.
 */
CK_EXPORT int ck_network_compose_chains(const CK_NetworkOrgan* net,
                                          int8_t* out_chain, int max_len) {
    const CK_NetworkState* s = &net->state;
    int len = 0;

    /* Traffic triple */
    float total_rate = s->send_rate_mbps + s->recv_rate_mbps;
    int traffic_op = (total_rate < 0.01f) ? CK_VOID :
                     (total_rate < 1.0f) ? CK_BREATH :
                     (total_rate < 10.0f) ? CK_PROGRESS :
                     (total_rate < 50.0f) ? CK_LATTICE : CK_CHAOS;
    int conn_op = (s->connection_count < 10) ? CK_VOID :
                  (s->established < 20) ? CK_BALANCE :
                  (s->established < 100) ? CK_PROGRESS :
                  (s->established < 500) ? CK_LATTICE : CK_CHAOS;
    int coupling = CL[traffic_op][conn_op];

    if (len + 3 <= max_len) {
        out_chain[len++] = (int8_t)traffic_op;
        out_chain[len++] = (int8_t)conn_op;
        out_chain[len++] = (int8_t)coupling;
    }

    /* Jitter operator */
    int jitter_op;
    if (s->jitter > 0.5f) jitter_op = CK_CHAOS;
    else if (s->jitter > 0.2f) jitter_op = CK_COLLAPSE;
    else if (s->jitter > 0.1f) jitter_op = CK_COUNTER;
    else jitter_op = CK_HARMONY;

    if (len + 2 <= max_len) {
        out_chain[len++] = (int8_t)jitter_op;
        out_chain[len++] = (int8_t)CL[jitter_op][coupling];
    }

    /* Topology health indicators */
    if (s->time_wait > 50 && len < max_len) out_chain[len++] = CK_RESET;
    if (s->close_wait > 20 && len < max_len) out_chain[len++] = CK_COLLAPSE;
    if (s->established > 100 && len < max_len) out_chain[len++] = CK_LATTICE;

    /* Recent operator chain */
    for (int i = 0; i < net->op_chain_count && len < max_len; i++) {
        int idx = (net->op_chain_head - net->op_chain_count + i + CK_NET_OP_CHAIN_LEN)
                  % CK_NET_OP_CHAIN_LEN;
        out_chain[len++] = net->op_chain[idx];
    }

    return len;
}


/* ═══════════════════════════════════════════════════════════════
 * §4  GPU OBSERVATION
 * ═══════════════════════════════════════════════════════════════
 *
 * Reads CK's muscle (GPU) state.
 * Currently uses simplified metrics from process observation.
 * Full NVML direct reads planned for Phase 4.
 */

/**
 * ck_gpu_classify — map GPU state to TIG operator.
 * Same logic as Gen6b operator_for_state().
 */
CK_EXPORT int ck_gpu_classify(const CK_GPUState* s) {
    if (s->gpu_util_pct < 10) return CK_VOID;          /* IDLE */
    if (s->temperature_c > 80 || s->throttle_thermal)
        return CK_COLLAPSE;                              /* THERMAL */
    if (s->throttle_power) return CK_RESET;             /* THROTTLE */
    if (s->gpu_util_pct < 50) return CK_BALANCE;       /* CRUISE */
    if (s->gpu_util_pct < 85) return CK_PROGRESS;      /* COMPUTE */
    return CK_COLLAPSE;                                  /* OVERLOADED */
}


/* ═══════════════════════════════════════════════════════════════
 * §5  INTEGRATED OBSERVER TICK — feeds heartbeat
 * ═══════════════════════════════════════════════════════════════
 *
 * Called from ck_heartbeat_tick(). Observes all three organs:
 *   1. Processes (every tick)
 *   2. Network (every 5 ticks)
 *   3. GPU (every 10 ticks)
 *
 * Feeds operator chains to TL. Returns system coherence.
 */

CK_EXPORT float ck_observer_full_tick(CK_Organism* org) {
    CK_SystemObserver* obs = &org->observer;

    /* Always observe processes */
    int sys_op = ck_observer_tick(obs);

    /* Feed process operators to TL */
    int8_t proc_ops[CK_MAX_PROCESSES];
    int n_ops = ck_observer_all_ops(obs, proc_ops, CK_MAX_PROCESSES);
    if (n_ops >= 3) {
        /* Feed last 20 operators (or fewer) */
        int start = (n_ops > 20) ? n_ops - 20 : 0;
        ck_tl_eat_ops(&org->tl, &proc_ops[start], n_ops - start);
    }

    /* Feed body domain */
    ck_bridge_feed(&org->bridge, "processes", sys_op);

    /* ── OPERATOR DIVERSITY → BODY UPDATE ─────────────────
     * The body's E/A/K must reflect what the observer actually sees.
     * Without this, body.C is frozen at init value forever.
     *
     *   E (entropy) = how disordered the process distribution is
     *   A (alignment) = pairwise CL harmony ratio (observer_coherence)
     *   K (knowledge) = grows with observations, asymptotes at 1.0
     */
    if (n_ops >= 2) {
        /* E: count how many distinct operators are active */
        int op_counts[CK_NUM_OPS];
        memset(op_counts, 0, sizeof(op_counts));
        for (int i = 0; i < n_ops; i++) {
            if (proc_ops[i] >= 0 && proc_ops[i] < CK_NUM_OPS)
                op_counts[(int)proc_ops[i]]++;
        }
        int distinct = 0;
        for (int i = 0; i < CK_NUM_OPS; i++) {
            if (op_counts[i] > 0) distinct++;
        }
        /* Shannon entropy of operator distribution, normalized to [0,1] */
        float H = 0.0f;
        for (int i = 0; i < CK_NUM_OPS; i++) {
            if (op_counts[i] > 0) {
                float p = (float)op_counts[i] / (float)n_ops;
                H -= p * logf(p);
            }
        }
        float max_H = logf((float)(distinct > 1 ? distinct : 2));
        float norm_H = (max_H > 0.0f) ? H / max_H : 0.0f;

        /* A: pairwise CL coupling = observer_coherence */
        float obs_coh = ck_observer_coherence(obs);

        /* K: grows with observation count, asymptotes at 1.0 */
        float K_target = 1.0f - 1.0f / (1.0f + (float)obs->tick * 0.01f);

        /* Smooth update (don't slam — blend toward measured values) */
        float blend = 0.3f;  /* 30% new, 70% old per tick */
        org->body.E = org->body.E * (1.0f - blend) + norm_H * blend;
        org->body.A = org->body.A * (1.0f - blend) + obs_coh * blend;
        org->body.K = org->body.K * (1.0f - blend) + K_target * blend;

        /* Clamp */
        if (org->body.E < 0.0f) org->body.E = 0.0f;
        if (org->body.E > 1.0f) org->body.E = 1.0f;
        if (org->body.A < 0.0f) org->body.A = 0.0f;
        if (org->body.A > 1.0f) org->body.A = 1.0f;
        if (org->body.K < 0.0f) org->body.K = 0.0f;
        if (org->body.K > 1.0f) org->body.K = 1.0f;

        /* Recompute body coherence: C = 0.4*(1-E) + 0.35*A + 0.25*K */
        org->body.C = ck_coherence_eak(org->body.E, org->body.A, org->body.K);
        org->body.band = ck_band(org->body.C);
        org->body.ticks++;
    }

    /* Network read every 5 ticks */
    if (obs->tick % 5 == 0) {
        ck_network_read(&org->network);
        if (org->network.available) {
            int net_op = org->network.state.op;
            ck_network_compose(org, net_op);

            /* Feed network chains */
            int8_t net_chains[32];
            int net_len = ck_network_compose_chains(&org->network, net_chains, 32);
            if (net_len >= 2) {
                ck_tl_eat_ops(&org->tl, net_chains, net_len);
            }
        }
    }

    /* GPU read every 10 ticks (simplified — full NVML in Phase 4) */
    if (obs->tick % 10 == 0 && org->gpu.available) {
        int gpu_op = ck_gpu_classify(&org->gpu.state);
        ck_gpu_compose(org, gpu_op);
    }

    return ck_observer_coherence(obs);
}
