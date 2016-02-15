Register map
===========

Register Map
------------

## 0x0 chip_id_reg

This register cotains the part # and revision # for XYZ ASIC

Bits | Access | Name | Description
-----|--------|------|------------
3:0|read-only|rev_num|This field represents the chips revision number
31:4|read-only|part_num|This field represents the chips part number

## 0x4 link_status

Bits | Access | Name | Description
-----|--------|------|------------
3:0|read-only|port0|Status of a Serdes Link
7:4|read-only|port1|Status of a Serdes Link
11:8|read-only|port2|Status of a Serdes Link
15:12|read-only|port3|Status of a Serdes Link

## 0x10 myRegInst

Bits | Access | Name | Description
-----|--------|------|------------
1:0|read-write|data0|My example 2bit status field
3:2|read-write|data1|My example 2bit status field
5:4|read-write|data2|My example 2bit status field
7:6|read-write|data3|My example 2bit status field
9:8|read-write|data4|My example 2bit status field
11:10|read-write|data5|My example 2bit status field
13:12|read-write|data6|My example 2bit status field
15:14|read-write|data7|My example 2bit status field
17:16|read-write|data8|My example 2bit status field
19:18|read-write|data9|My example 2bit status field
21:20|read-write|data10|My example 2bit status field
23:22|read-write|data11|My example 2bit status field
25:24|read-write|data12|My example 2bit status field
27:26|read-write|data13|My example 2bit status field
29:28|read-write|data14|My example 2bit status field
31:30|read-write|data15|My example 2bit status field

## 0x20 spi4_pkt_count

Bits | Access | Name | Description
-----|--------|------|------------
15:0|read-write|port1|Number of certain packet type seen
31:16|read-write|port0|Number of certain packet type seen

## 0x24 gige_pkt_count_reg

Bits | Access | Name | Description
-----|--------|------|------------
7:0|read-write|port3|Number of certain packet type seen
15:8|read-write|port2|Number of certain packet type seen
23:16|read-write|port1|Number of certain packet type seen
31:24|read-write|port0|Number of certain packet type seen

## 0x100 fifo_port_0_head

Bits | Access | Name | Description
-----|--------|------|------------
31:0|read-write|data|

## 0x104 fifo_port_0_tail

Bits | Access | Name | Description
-----|--------|------|------------
31:0|read-write|data|

## 0x108 fifo_port_0_status

Bits | Access | Name | Description
-----|--------|------|------------
0|read-write|full|
1|read-write|empty|
4|read-write|almost_empty|
5|read-write|almost_full|

## 0x110 fifo_port_1_head

Bits | Access | Name | Description
-----|--------|------|------------
31:0|read-write|data|

## 0x114 fifo_port_1_tail

Bits | Access | Name | Description
-----|--------|------|------------
31:0|read-write|data|

## 0x118 fifo_port_1_status

Bits | Access | Name | Description
-----|--------|------|------------
0|read-write|full|
1|read-write|empty|
4|read-write|almost_empty|
5|read-write|almost_full|

## 0x120 fifo_port_2_head

Bits | Access | Name | Description
-----|--------|------|------------
31:0|read-write|data|

## 0x124 fifo_port_2_tail

Bits | Access | Name | Description
-----|--------|------|------------
31:0|read-write|data|

## 0x128 fifo_port_2_status

Bits | Access | Name | Description
-----|--------|------|------------
0|read-write|full|
1|read-write|empty|
4|read-write|almost_empty|
5|read-write|almost_full|

## 0x130 fifo_port_3_head

Bits | Access | Name | Description
-----|--------|------|------------
31:0|read-write|data|

## 0x134 fifo_port_3_tail

Bits | Access | Name | Description
-----|--------|------|------------
31:0|read-write|data|

## 0x138 fifo_port_3_status

Bits | Access | Name | Description
-----|--------|------|------------
0|read-write|full|
1|read-write|empty|
4|read-write|almost_empty|
5|read-write|almost_full|

## 0x140 fifo_port_4_head

Bits | Access | Name | Description
-----|--------|------|------------
31:0|read-write|data|

## 0x144 fifo_port_4_tail

Bits | Access | Name | Description
-----|--------|------|------------
31:0|read-write|data|

## 0x148 fifo_port_4_status

Bits | Access | Name | Description
-----|--------|------|------------
0|read-write|full|
1|read-write|empty|
4|read-write|almost_empty|
5|read-write|almost_full|

## 0x150 fifo_port_5_head

Bits | Access | Name | Description
-----|--------|------|------------
31:0|read-write|data|

## 0x154 fifo_port_5_tail

Bits | Access | Name | Description
-----|--------|------|------------
31:0|read-write|data|

## 0x158 fifo_port_5_status

Bits | Access | Name | Description
-----|--------|------|------------
0|read-write|full|
1|read-write|empty|
4|read-write|almost_empty|
5|read-write|almost_full|

## 0x160 fifo_port_6_head

Bits | Access | Name | Description
-----|--------|------|------------
31:0|read-write|data|

## 0x164 fifo_port_6_tail

Bits | Access | Name | Description
-----|--------|------|------------
31:0|read-write|data|

## 0x168 fifo_port_6_status

Bits | Access | Name | Description
-----|--------|------|------------
0|read-write|full|
1|read-write|empty|
4|read-write|almost_empty|
5|read-write|almost_full|

## 0x170 fifo_port_7_head

Bits | Access | Name | Description
-----|--------|------|------------
31:0|read-write|data|

## 0x174 fifo_port_7_tail

Bits | Access | Name | Description
-----|--------|------|------------
31:0|read-write|data|

## 0x178 fifo_port_7_status

Bits | Access | Name | Description
-----|--------|------|------------
0|read-write|full|
1|read-write|empty|
4|read-write|almost_empty|
5|read-write|almost_full|

## 0x1000 vc_pkt_count_0

Bits | Access | Name | Description
-----|--------|------|------------
30:0|read-write|vc_count|Number of certain packet type seen
31|read-write|active|VC is Active

## 0x1010 vc_pkt_count_1

Bits | Access | Name | Description
-----|--------|------|------------
30:0|read-write|vc_count|Number of certain packet type seen
31|read-write|active|VC is Active

## 0x1020 vc_pkt_count_2

Bits | Access | Name | Description
-----|--------|------|------------
30:0|read-write|vc_count|Number of certain packet type seen
31|read-write|active|VC is Active

## 0x1030 vc_pkt_count_3

Bits | Access | Name | Description
-----|--------|------|------------
30:0|read-write|vc_count|Number of certain packet type seen
31|read-write|active|VC is Active

## 0x1040 vc_pkt_count_4

Bits | Access | Name | Description
-----|--------|------|------------
30:0|read-write|vc_count|Number of certain packet type seen
31|read-write|active|VC is Active

## 0x1050 vc_pkt_count_5

Bits | Access | Name | Description
-----|--------|------|------------
30:0|read-write|vc_count|Number of certain packet type seen
31|read-write|active|VC is Active

## 0x1060 vc_pkt_count_6

Bits | Access | Name | Description
-----|--------|------|------------
30:0|read-write|vc_count|Number of certain packet type seen
31|read-write|active|VC is Active

## 0x1070 vc_pkt_count_7

Bits | Access | Name | Description
-----|--------|------|------------
30:0|read-write|vc_count|Number of certain packet type seen
31|read-write|active|VC is Active

## 0x1080 vc_pkt_count_8

Bits | Access | Name | Description
-----|--------|------|------------
30:0|read-write|vc_count|Number of certain packet type seen
31|read-write|active|VC is Active

## 0x1090 vc_pkt_count_9

Bits | Access | Name | Description
-----|--------|------|------------
30:0|read-write|vc_count|Number of certain packet type seen
31|read-write|active|VC is Active

## 0x10a0 vc_pkt_count_10

Helpful description

Bits | Access | Name | Description
-----|--------|------|------------
30:0|read-write|vc_count|Number of certain packet type seen
31|read-write|active|VC is Active

