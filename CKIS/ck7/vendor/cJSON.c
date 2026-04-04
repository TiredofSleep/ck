/*
  Copyright (c) 2009-2017 Dave Gamble and cJSON contributors
  MIT License (see cJSON.h)

  Minimal cJSON implementation for CK Gen7.
  Supports: parse JSON, create JSON, print JSON.
  Covers: objects, arrays, numbers, strings, booleans, null.
*/

#include "cJSON.h"
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <float.h>
#include <limits.h>
#include <ctype.h>

/* ── Internal allocation ─────────────────────────────── */

static cJSON* cJSON_New_Item(void) {
    cJSON* node = (cJSON*)calloc(1, sizeof(cJSON));
    return node;
}

void cJSON_Delete(cJSON *item) {
    cJSON *next;
    while (item) {
        next = item->next;
        if (!(item->type & cJSON_IsReference) && item->child)
            cJSON_Delete(item->child);
        if (!(item->type & cJSON_IsReference) && item->valuestring)
            free(item->valuestring);
        if (!(item->type & cJSON_StringIsConst) && item->string)
            free(item->string);
        free(item);
        item = next;
    }
}

static char* cJSON_strdup(const char *str) {
    size_t len = strlen(str) + 1;
    char *copy = (char*)malloc(len);
    if (copy) memcpy(copy, str, len);
    return copy;
}

/* ── Parse helpers ───────────────────────────────────── */

static const char* skip_whitespace(const char *in) {
    while (in && *in && (unsigned char)*in <= 32) in++;
    return in;
}

static const char* parse_number(cJSON *item, const char *num) {
    double n = 0;
    int sign = 1, scale = 0, subscale = 0, signsubscale = 1;

    if (*num == '-') { sign = -1; num++; }
    if (*num == '0') { num++; }
    if (*num >= '1' && *num <= '9') {
        do { n = n * 10.0 + (*num++ - '0'); } while (*num >= '0' && *num <= '9');
    }
    if (*num == '.' && num[1] >= '0' && num[1] <= '9') {
        num++;
        do { n = n * 10.0 + (*num++ - '0'); scale--; } while (*num >= '0' && *num <= '9');
    }
    if (*num == 'e' || *num == 'E') {
        num++;
        if (*num == '+') num++;
        else if (*num == '-') { signsubscale = -1; num++; }
        while (*num >= '0' && *num <= '9') { subscale = subscale * 10 + (*num++ - '0'); }
    }

    n = sign * n * pow(10.0, scale + subscale * signsubscale);
    item->valuedouble = n;
    item->valueint = (int)n;
    item->type = cJSON_Number;
    return num;
}

static unsigned parse_hex4(const char *str) {
    unsigned h = 0;
    for (int i = 0; i < 4; i++) {
        if (*str >= '0' && *str <= '9') h = h * 16 + (*str - '0');
        else if (*str >= 'A' && *str <= 'F') h = h * 16 + 10 + (*str - 'A');
        else if (*str >= 'a' && *str <= 'f') h = h * 16 + 10 + (*str - 'a');
        else return 0;
        str++;
    }
    return h;
}

static const char* parse_string(cJSON *item, const char *str) {
    const char *ptr = str + 1;
    char *ptr2, *out;
    int len = 0;
    unsigned uc, uc2;

    if (*str != '\"') return NULL;

    /* Count length */
    while (*ptr != '\"' && *ptr) {
        if (*ptr++ == '\\') ptr++;
        len++;
    }
    if (!*ptr) return NULL;

    out = (char*)malloc(len + 1);
    if (!out) return NULL;

    ptr = str + 1;
    ptr2 = out;
    while (*ptr != '\"' && *ptr) {
        if (*ptr != '\\') { *ptr2++ = *ptr++; }
        else {
            ptr++;
            switch (*ptr) {
                case 'b': *ptr2++ = '\b'; break;
                case 'f': *ptr2++ = '\f'; break;
                case 'n': *ptr2++ = '\n'; break;
                case 'r': *ptr2++ = '\r'; break;
                case 't': *ptr2++ = '\t'; break;
                case 'u':
                    uc = parse_hex4(ptr + 1); ptr += 4;
                    if (uc >= 0xDC00 && uc <= 0xDFFF) break;
                    if (uc >= 0xD800 && uc <= 0xDBFF) {
                        if (ptr[1] != '\\' || ptr[2] != 'u') break;
                        uc2 = parse_hex4(ptr + 3); ptr += 6;
                        if (uc2 < 0xDC00 || uc2 > 0xDFFF) break;
                        uc = 0x10000 + (((uc & 0x3FF) << 10) | (uc2 & 0x3FF));
                    }
                    if (uc < 0x80) *ptr2++ = (char)uc;
                    else if (uc < 0x800) { *ptr2++ = (char)(0xC0 | (uc >> 6)); *ptr2++ = (char)(0x80 | (uc & 0x3F)); }
                    else if (uc < 0x10000) { *ptr2++ = (char)(0xE0 | (uc >> 12)); *ptr2++ = (char)(0x80 | ((uc >> 6) & 0x3F)); *ptr2++ = (char)(0x80 | (uc & 0x3F)); }
                    else { *ptr2++ = (char)(0xF0 | (uc >> 18)); *ptr2++ = (char)(0x80 | ((uc >> 12) & 0x3F)); *ptr2++ = (char)(0x80 | ((uc >> 6) & 0x3F)); *ptr2++ = (char)(0x80 | (uc & 0x3F)); }
                    break;
                default: *ptr2++ = *ptr; break;
            }
            ptr++;
        }
    }
    *ptr2 = 0;
    if (*ptr == '\"') ptr++;
    item->valuestring = out;
    item->type = cJSON_String;
    return ptr;
}

static const char* parse_value(cJSON *item, const char *value);

static const char* parse_array(cJSON *item, const char *value) {
    cJSON *child;
    if (*value != '[') return NULL;
    item->type = cJSON_Array;
    value = skip_whitespace(value + 1);
    if (*value == ']') return value + 1;

    item->child = child = cJSON_New_Item();
    if (!child) return NULL;
    value = skip_whitespace(parse_value(child, skip_whitespace(value)));
    if (!value) return NULL;

    while (*value == ',') {
        cJSON *new_item = cJSON_New_Item();
        if (!new_item) return NULL;
        child->next = new_item;
        new_item->prev = child;
        child = new_item;
        value = skip_whitespace(parse_value(child, skip_whitespace(value + 1)));
        if (!value) return NULL;
    }

    if (*value == ']') return value + 1;
    return NULL;
}

static const char* parse_object(cJSON *item, const char *value) {
    cJSON *child;
    if (*value != '{') return NULL;
    item->type = cJSON_Object;
    value = skip_whitespace(value + 1);
    if (*value == '}') return value + 1;

    item->child = child = cJSON_New_Item();
    if (!child) return NULL;
    value = skip_whitespace(parse_string(child, skip_whitespace(value)));
    if (!value) return NULL;
    child->string = child->valuestring;
    child->valuestring = NULL;
    if (*value != ':') return NULL;
    value = skip_whitespace(parse_value(child, skip_whitespace(value + 1)));
    if (!value) return NULL;

    while (*value == ',') {
        cJSON *new_item = cJSON_New_Item();
        if (!new_item) return NULL;
        child->next = new_item;
        new_item->prev = child;
        child = new_item;
        value = skip_whitespace(parse_string(child, skip_whitespace(value + 1)));
        if (!value) return NULL;
        child->string = child->valuestring;
        child->valuestring = NULL;
        if (*value != ':') return NULL;
        value = skip_whitespace(parse_value(child, skip_whitespace(value + 1)));
        if (!value) return NULL;
    }

    if (*value == '}') return value + 1;
    return NULL;
}

static const char* parse_value(cJSON *item, const char *value) {
    if (!value) return NULL;
    if (!strncmp(value, "null", 4))  { item->type = cJSON_NULL; return value + 4; }
    if (!strncmp(value, "false", 5)) { item->type = cJSON_False; return value + 5; }
    if (!strncmp(value, "true", 4))  { item->type = cJSON_True; item->valueint = 1; return value + 4; }
    if (*value == '\"') return parse_string(item, value);
    if (*value == '-' || (*value >= '0' && *value <= '9')) return parse_number(item, value);
    if (*value == '[') return parse_array(item, value);
    if (*value == '{') return parse_object(item, value);
    return NULL;
}

cJSON* cJSON_Parse(const char *value) {
    cJSON *c = cJSON_New_Item();
    if (!c) return NULL;
    if (!parse_value(c, skip_whitespace(value))) {
        cJSON_Delete(c);
        return NULL;
    }
    return c;
}

/* ── Print helpers ───────────────────────────────────── */

typedef struct {
    char *buffer;
    size_t length;
    size_t offset;
} printbuffer;

static void ensure_buf(printbuffer *p, size_t needed) {
    if (p->offset + needed >= p->length) {
        size_t newsize = p->length * 2;
        if (newsize < p->offset + needed + 64) newsize = p->offset + needed + 64;
        char *nb = (char*)realloc(p->buffer, newsize);
        if (nb) { p->buffer = nb; p->length = newsize; }
    }
}

static void print_number(cJSON *item, printbuffer *p) {
    char num[64];
    double d = item->valuedouble;
    if (d == 0) {
        if (item->valueint == 0) strcpy(num, "0");
        else snprintf(num, sizeof(num), "%d", item->valueint);
    } else if (fabs(((double)item->valueint) - d) <= DBL_EPSILON && d <= INT_MAX && d >= INT_MIN) {
        snprintf(num, sizeof(num), "%d", item->valueint);
    } else if (fabs(floor(d) - d) <= DBL_EPSILON && fabs(d) < 1.0e15) {
        snprintf(num, sizeof(num), "%.0f", d);
    } else {
        snprintf(num, sizeof(num), "%g", d);
    }
    size_t len = strlen(num);
    ensure_buf(p, len + 1);
    memcpy(p->buffer + p->offset, num, len);
    p->offset += len;
}

static void print_string_ptr(const char *str, printbuffer *p) {
    if (!str) { ensure_buf(p, 3); memcpy(p->buffer + p->offset, "\"\"", 2); p->offset += 2; return; }
    size_t len = strlen(str);
    ensure_buf(p, len * 2 + 3);
    p->buffer[p->offset++] = '\"';
    for (size_t i = 0; i < len; i++) {
        char c = str[i];
        if (c == '\\' || c == '\"') { p->buffer[p->offset++] = '\\'; p->buffer[p->offset++] = c; }
        else if (c == '\n') { p->buffer[p->offset++] = '\\'; p->buffer[p->offset++] = 'n'; }
        else if (c == '\r') { p->buffer[p->offset++] = '\\'; p->buffer[p->offset++] = 'r'; }
        else if (c == '\t') { p->buffer[p->offset++] = '\\'; p->buffer[p->offset++] = 't'; }
        else p->buffer[p->offset++] = c;
    }
    p->buffer[p->offset++] = '\"';
}

static void print_value(cJSON *item, printbuffer *p);

static void print_array(cJSON *item, printbuffer *p) {
    ensure_buf(p, 2);
    p->buffer[p->offset++] = '[';
    cJSON *child = item->child;
    while (child) {
        print_value(child, p);
        child = child->next;
        if (child) { ensure_buf(p, 2); p->buffer[p->offset++] = ','; }
    }
    ensure_buf(p, 2);
    p->buffer[p->offset++] = ']';
}

static void print_object(cJSON *item, printbuffer *p) {
    ensure_buf(p, 2);
    p->buffer[p->offset++] = '{';
    cJSON *child = item->child;
    while (child) {
        print_string_ptr(child->string, p);
        ensure_buf(p, 2);
        p->buffer[p->offset++] = ':';
        print_value(child, p);
        child = child->next;
        if (child) { ensure_buf(p, 2); p->buffer[p->offset++] = ','; }
    }
    ensure_buf(p, 2);
    p->buffer[p->offset++] = '}';
}

static void print_value(cJSON *item, printbuffer *p) {
    if (!item) return;
    switch (item->type & 0xFF) {
        case cJSON_NULL:   ensure_buf(p, 5); memcpy(p->buffer + p->offset, "null", 4); p->offset += 4; break;
        case cJSON_False:  ensure_buf(p, 6); memcpy(p->buffer + p->offset, "false", 5); p->offset += 5; break;
        case cJSON_True:   ensure_buf(p, 5); memcpy(p->buffer + p->offset, "true", 4); p->offset += 4; break;
        case cJSON_Number: print_number(item, p); break;
        case cJSON_String: print_string_ptr(item->valuestring, p); break;
        case cJSON_Array:  print_array(item, p); break;
        case cJSON_Object: print_object(item, p); break;
        default: break;
    }
}

char* cJSON_PrintUnformatted(const cJSON *item) {
    printbuffer p = {0};
    p.buffer = (char*)malloc(256);
    p.length = 256;
    p.offset = 0;
    if (!p.buffer) return NULL;
    print_value((cJSON*)item, &p);
    ensure_buf(&p, 1);
    p.buffer[p.offset] = '\0';
    return p.buffer;
}

char* cJSON_Print(const cJSON *item) {
    /* For simplicity, same as unformatted in this minimal build */
    return cJSON_PrintUnformatted(item);
}

/* ── Query API ───────────────────────────────────────── */

int cJSON_GetArraySize(const cJSON *array) {
    if (!array) return 0;
    cJSON *c = array->child;
    int i = 0;
    while (c) { i++; c = c->next; }
    return i;
}

cJSON* cJSON_GetArrayItem(const cJSON *array, int index) {
    if (!array) return NULL;
    cJSON *c = array->child;
    while (c && index > 0) { index--; c = c->next; }
    return c;
}

cJSON* cJSON_GetObjectItem(const cJSON *object, const char *string) {
    if (!object || !string) return NULL;
    cJSON *c = object->child;
    while (c) {
        if (c->string && strcmp(c->string, string) == 0) return c;
        c = c->next;
    }
    return NULL;
}

int cJSON_IsArray(const cJSON *item)  { return item ? (item->type & 0xFF) == cJSON_Array  : 0; }
int cJSON_IsObject(const cJSON *item) { return item ? (item->type & 0xFF) == cJSON_Object : 0; }
int cJSON_IsNumber(const cJSON *item) { return item ? (item->type & 0xFF) == cJSON_Number : 0; }
int cJSON_IsString(const cJSON *item) { return item ? (item->type & 0xFF) == cJSON_String : 0; }

/* ── Create API ──────────────────────────────────────── */

cJSON* cJSON_CreateObject(void) {
    cJSON *item = cJSON_New_Item();
    if (item) item->type = cJSON_Object;
    return item;
}

cJSON* cJSON_CreateArray(void) {
    cJSON *item = cJSON_New_Item();
    if (item) item->type = cJSON_Array;
    return item;
}

cJSON* cJSON_CreateNumber(double num) {
    cJSON *item = cJSON_New_Item();
    if (item) { item->type = cJSON_Number; item->valuedouble = num; item->valueint = (int)num; }
    return item;
}

cJSON* cJSON_CreateString(const char *string) {
    cJSON *item = cJSON_New_Item();
    if (item) { item->type = cJSON_String; item->valuestring = cJSON_strdup(string ? string : ""); }
    return item;
}

cJSON* cJSON_CreateBool(int boolean) {
    cJSON *item = cJSON_New_Item();
    if (item) { item->type = boolean ? cJSON_True : cJSON_False; item->valueint = boolean ? 1 : 0; }
    return item;
}

cJSON* cJSON_CreateNull(void) {
    cJSON *item = cJSON_New_Item();
    if (item) item->type = cJSON_NULL;
    return item;
}

static void suffix_object(cJSON *prev, cJSON *item) {
    prev->next = item;
    item->prev = prev;
}

void cJSON_AddItemToArray(cJSON *array, cJSON *item) {
    if (!item || !array) return;
    cJSON *child = array->child;
    if (!child) { array->child = item; }
    else {
        while (child->next) child = child->next;
        suffix_object(child, item);
    }
}

void cJSON_AddItemToObject(cJSON *object, const char *string, cJSON *item) {
    if (!item || !object) return;
    if (item->string) free(item->string);
    item->string = cJSON_strdup(string);
    cJSON_AddItemToArray(object, item);
}

cJSON* cJSON_AddNumberToObject(cJSON *object, const char *name, double number) {
    cJSON *n = cJSON_CreateNumber(number);
    if (n) cJSON_AddItemToObject(object, name, n);
    return n;
}

cJSON* cJSON_AddStringToObject(cJSON *object, const char *name, const char *string) {
    cJSON *s = cJSON_CreateString(string);
    if (s) cJSON_AddItemToObject(object, name, s);
    return s;
}

cJSON* cJSON_AddBoolToObject(cJSON *object, const char *name, int boolean) {
    cJSON *b = cJSON_CreateBool(boolean);
    if (b) cJSON_AddItemToObject(object, name, b);
    return b;
}
