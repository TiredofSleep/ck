/*
  Copyright (c) 2009-2017 Dave Gamble and cJSON contributors

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in
  all copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
  THE SOFTWARE.

  cJSON — Ultralightweight JSON parser in ANSI C.
  This is a MINIMAL SUBSET for CK's needs (parse/create objects, arrays, numbers).
*/

#ifndef cJSON__h
#define cJSON__h

#ifdef __cplusplus
extern "C" {
#endif

#include <stddef.h>

/* cJSON Types: */
#define cJSON_Invalid (0)
#define cJSON_False  (1 << 0)
#define cJSON_True   (1 << 1)
#define cJSON_NULL   (1 << 2)
#define cJSON_Number (1 << 3)
#define cJSON_String (1 << 4)
#define cJSON_Array  (1 << 5)
#define cJSON_Object (1 << 6)
#define cJSON_Raw    (1 << 7)

#define cJSON_IsReference 256
#define cJSON_StringIsConst 512

typedef struct cJSON {
    struct cJSON *next;
    struct cJSON *prev;
    struct cJSON *child;
    int type;
    char *valuestring;
    int valueint;
    double valuedouble;
    char *string;   /* key name */
} cJSON;

/* API */
cJSON* cJSON_Parse(const char *value);
char*  cJSON_Print(const cJSON *item);
char*  cJSON_PrintUnformatted(const cJSON *item);
void   cJSON_Delete(cJSON *item);

int    cJSON_GetArraySize(const cJSON *array);
cJSON* cJSON_GetArrayItem(const cJSON *array, int index);
cJSON* cJSON_GetObjectItem(const cJSON *object, const char *string);

int    cJSON_IsArray(const cJSON *item);
int    cJSON_IsObject(const cJSON *item);
int    cJSON_IsNumber(const cJSON *item);
int    cJSON_IsString(const cJSON *item);

cJSON* cJSON_CreateObject(void);
cJSON* cJSON_CreateArray(void);
cJSON* cJSON_CreateNumber(double num);
cJSON* cJSON_CreateString(const char *string);
cJSON* cJSON_CreateBool(int boolean);
cJSON* cJSON_CreateNull(void);

cJSON* cJSON_AddNumberToObject(cJSON *object, const char *name, double number);
cJSON* cJSON_AddStringToObject(cJSON *object, const char *name, const char *string);
cJSON* cJSON_AddBoolToObject(cJSON *object, const char *name, int boolean);
void   cJSON_AddItemToObject(cJSON *object, const char *string, cJSON *item);
void   cJSON_AddItemToArray(cJSON *array, cJSON *item);

#ifdef __cplusplus
}
#endif

#endif
