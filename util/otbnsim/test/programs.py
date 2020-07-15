# Copyright lowRISC contributors.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0

import argparse
import sys

from otbnsim.asm import parse, output

w04_prolog = """
addi x4, x0, 0
bn.lid x4, 0(x0)
addi x4, x0, 1
bn.lid x4, 1(x0)
addi x4, x0, 2
bn.lid x4, 2(x0)
addi x4, x0, 3
bn.lid x4, 3(x0)
"""

w04_epilog = """
addi x4, x0, 0
bn.sid x4, 0(x0)
addi x4, x0, 1
bn.sid x4, 1(x0)
addi x4, x0, 2
bn.sid x4, 3(x0)
addi x4, x0, 3
bn.sid x4, 3(x0)
"""

code_mul_256x256 = """
BN.MULQACC.Z w0.0, w1.0, 0
BN.MULQACC w0.1, w1.0, 64
BN.MULQACC.SO w2.l, w0.0, w1.1, 64
BN.MULQACC w0.2, w1.0, 0
BN.MULQACC w0.1, w1.1, 0
BN.MULQACC w0.0, w1.2, 0
BN.MULQACC w0.3, w1.0, 64
BN.MULQACC w0.2, w1.1, 64
BN.MULQACC w0.1, w1.2, 64
BN.MULQACC.SO w2.u, w0.0, w1.3, 64
BN.MULQACC w0.3, w1.1, 0
BN.MULQACC w0.2, w1.2, 0
BN.MULQACC w0.1, w1.3, 0
BN.MULQACC w0.3, w1.2, 64
BN.MULQACC.SO w3.l, w0.2, w1.3, 64
BN.MULQACC.SO w3.u, w0.3, w1.3, 0
"""

if __name__ == "__main__":
    codes = [code[5:] for code in dir() if code.startswith("code_")]
    parser = argparse.ArgumentParser()
    parser.add_argument("test", type=str, choices=codes)
    parser.add_argument("outfile",
                        nargs="?",
                        type=argparse.FileType('wb'),
                        default=sys.stdout)
    parser.add_argument("-s",
                        "--standalone",
                        action="store_true",
                        help="Generate standalone (w0-w4 calling) code")
    parser.add_argument("-O",
                        "--output-format",
                        choices=["asm", "binary", "carray"],
                        default="asm")

    args = parser.parse_args()
    code = parse(globals()["code_"+args.test])
    if args.standalone:
        code = w04_prolog + code + w04_epilog
    output(code, args.outfile, args.output_format)
