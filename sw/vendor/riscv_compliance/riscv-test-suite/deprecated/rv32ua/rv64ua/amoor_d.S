# See LICENSE for license details.

#*****************************************************************************
# amoor_d.S
#-----------------------------------------------------------------------------
#
# Test amoor.d instruction.
#

#include "riscv_test.h"
#include "test_macros.h"

RVTEST_RV64U
RV_COMPLIANCE_CODE_BEGIN

  TEST_CASE(2, a4, 0xffffffff80000000, \
    li a0, 0xffffffff80000000; \
    li a1, 0xfffffffffffff800; \
    la a3, amo_operand; \
    sd a0, 0(a3); \
    amoor.d	a4, a1, 0(a3); \
  )

  TEST_CASE(3, a5, 0xfffffffffffff800, ld a5, 0(a3))

  # try again after a cache miss
  TEST_CASE(4, a4, 0xfffffffffffff800, \
    li  a1, 1; \
    amoor.d a4, a1, 0(a3); \
  )

  TEST_CASE(5, a5, 0xfffffffffffff801, ld a5, 0(a3))

  TEST_PASSFAIL

RV_COMPLIANCE_CODE_END

  .data
RVTEST_DATA_BEGIN

  TEST_DATA

RVTEST_DATA_END

  .bss
  .align 3
amo_operand:
  .dword 0
