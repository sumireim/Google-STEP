//
// >>>> malloc challenge! <<<<
//
// Your task is to improve utilization and speed of the following malloc
// implementation.
// Initial implementation is the same as the one implemented in simple_malloc.c.
// For the detailed explanation, please refer to simple_malloc.c.

#include <assert.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//
// Interfaces to get memory pages from OS
//

void *mmap_from_system(size_t size); //osからメモリを取得
void munmap_to_system(void *ptr, size_t size); //osにメモリを返す

//
// Struct definitions
//

// デバッグ用変数
//static int bin_request_count[8] = {0};  // 各binへの要求回数
//static size_t total_requests = 0; 

//メモリブロック管理構造体
typedef struct my_metadata_t {
  size_t size;
  struct my_metadata_t *next; // 連結リスト
} my_metadata_t;

// メモリヒープ管理構造体
typedef struct my_heap_t {
  my_metadata_t *free_head; 
  my_metadata_t dummy;
} my_heap_t;

//
// Static variables (DO NOT ADD ANOTHER STATIC VARIABLES!)
//
my_heap_t my_heap[8]; // 8つのbinを持つヒープ

//
// Helper functions (feel free to add/remove/edit!)
//

// binのサイズを振り分け
int divide_into_bin(size_t size) {
  // 8 <= size <= 4000 かつ sizeは8の倍数である
  size_t multiple_size = size / 8;
  assert(multiple_size >= 1 && multiple_size <= 510); // エラーになったので、buffer_size = 4096を考慮して設定

  int bin_index;
  if (multiple_size <= 4) bin_index = 0;
  else if (multiple_size <= 8) bin_index = 1;
  else if (multiple_size == 16) bin_index = 2;
  else if (multiple_size <= 32) bin_index = 3;
  else if (multiple_size <= 64) bin_index = 4;
  else if (multiple_size <= 128) bin_index = 5; 
  else if (multiple_size <= 256) bin_index = 6; 
  else bin_index = 7; 

  /*bin_request_count[bin_index]++;
  total_requests++;
  if (total_requests % 3000 == 0) {
    printf("=== Request Statistics (after %zu requests) ===\n", total_requests);
    for (int i = 0; i < 5; i++) {
      printf("bin[%d]: %d requests (%.1f%%)\n", 
             i, bin_request_count[i], 
             100.0 * bin_request_count[i] / total_requests);
    }
    printf("\n");
  }*/

  return bin_index; 
}

void add_to_bin(my_metadata_t *metadata) {
  // サイズに応じてbinに追加
  int bin_index = divide_into_bin(metadata->size);
  assert(bin_index >= 0 && bin_index < 8);
  metadata->next = my_heap[bin_index].free_head;
  my_heap[bin_index].free_head = metadata;
}

void remove_from_bin(my_metadata_t *metadata, my_metadata_t *prev, int bin_index) {
  if (prev) {
    prev->next = metadata->next;
  } else {
    my_heap[bin_index].free_head = metadata->next;
  }
  metadata->next = NULL; 
}

my_metadata_t* find_best_block(size_t size) {
  int target_bin = divide_into_bin(size);
  
  my_metadata_t *best_block = NULL;
  my_metadata_t *best_prev = NULL;
  int best_bin = -1;
  size_t best_size = SIZE_MAX;
  
  // 適切なbinから探索し、空だったら次のbinへ
  for (int i = target_bin; i < 8; i++) {
    my_metadata_t *current = my_heap[i].free_head;
    my_metadata_t *prev = NULL;
    
    while (current && current->size > 0) {
      if (current->size >= size && current->size < best_size) {
        best_block = current;
        best_prev = prev;
        best_bin = i;
        best_size = current->size;
        
        // 完全に一致したとき
        if (current->size == size) {
          goto perfect;
        }
      }
      prev = current;
      current = current->next;
    }
  }
  
perfect:
  // ブロックをbinから削除
  if (best_block) {
    remove_from_bin(best_block, best_prev, best_bin);
  }
  return best_block;
}

//
// Interfaces of malloc (DO NOT RENAME FOLLOWING FUNCTIONS!)
//

// This is called at the beginning of each challenge.
void my_initialize() {
  for (int i = 0; i < 8; i++) {
    my_heap[i].free_head = &my_heap[i].dummy;
    my_heap[i].dummy.size = 0;
    my_heap[i].dummy.next = NULL;
  }
}

// my_malloc() is called every time an object is allocated.
// |size| is guaranteed to be a multiple of 8 bytes and meets 8 <= |size| <=
// 4000. You are not allowed to use any library functions other than
// mmap_from_system() / munmap_to_system().
// First-fit: Find the first free slot the object fits.
// TODO: Update this logic to Best-fit!
// now, metadata points to the first free slot
// and prev is the previous entry.
void *my_malloc(size_t size) {
  // printf("Requested size: %zu\n", size);  // デバッグ用
  // 適切なブロックを見つける
  my_metadata_t *metadata = find_best_block(size);
  // 全てのbinに空きがないとき、osにメモリを要求する
  if (!metadata) {
    // There was no free slot available. We need to request a new memory region
    // from the system by calling mmap_from_system().
    //
    //     | metadata | free slot |
    //     ^
    //     metadata
    //     <---------------------->
    //            buffer_size
    size_t buffer_size = 4096;
    my_metadata_t *metadata = (my_metadata_t *)mmap_from_system(buffer_size);
    metadata->size = buffer_size - sizeof(my_metadata_t);
    metadata->next = NULL;
    // 適切なbin(bin[7])に追加
    add_to_bin(metadata);
    // Now, try my_malloc() again. This should succeed.
    return my_malloc(size);
  }

  // |ptr| is the beginning of the allocated object.
  //
  // ... | metadata | object | ...
  //     ^          ^
  //     metadata   ptr
  
  void *ptr = metadata + 1; // ユーザーにmetadataの次のアドレスを返す
  size_t remaining_size = metadata->size - size; // 残っているサイズを計算

  // ブロック分割処理
  if (remaining_size > sizeof(my_metadata_t)) {
    // Shrink the metadata for the allocated object
    // to separate the rest of the region corresponding to remaining_size.
    // If the remaining_size is not large enough to make a new metadata,
    // this code path will not be taken and the region will be managed
    // as a part of the allocated object.
    metadata->size = size;
    // 残りの部分で新しいmetadataを作成
    //
    // ... | metadata | object | metadata | free slot | ...
    //     ^          ^        ^
    //     metadata   ptr      new_metadata
    //                 <------><---------------------->
    //                   size       remaining size
    my_metadata_t *new_metadata = (my_metadata_t *)((char *)ptr + size);
    new_metadata->size = remaining_size - sizeof(my_metadata_t);
    new_metadata->next = NULL;
    // 残りブロックをbinに追加
    add_to_bin(new_metadata);
  }
  return ptr;
}

// This is called every time an object is freed.  You are not allowed to
// use any library functions other than mmap_from_system / munmap_to_system.
void my_free(void *ptr) {
  // Look up the metadata. The metadata is placed just prior to the object.
  //
  // ... | metadata | object | ...
  //     ^          ^
  //     metadata   ptr
  // ポインタの直前にあるmetadataを取得
  my_metadata_t *metadata = (my_metadata_t *)ptr - 1;
  // binに追加
  add_to_bin(metadata);
}

// This is called at the end of each challenge.
void my_finalize() {
  // Nothing is here for now.
  // feel free to add something if you want!
}

void test() {
  // Implement here!
  assert(1 == 1); /* 1 is 1. That's always true! (You can remove this.) */
}
