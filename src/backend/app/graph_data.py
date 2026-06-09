"""
NetworkX-based knowledge graph, loaded from an in-memory JSON seed.

Node hierarchy:  domain -> course -> chapter -> knowledge_point
Edge types:      CONTAINS, PREREQUISITE, RELATED_TO
"""

from typing import List, Dict, Optional
import networkx as nx


# ---------------------------------------------------------------------------
# Seed data
# ---------------------------------------------------------------------------

SEED_DATA: Dict = {
    "nodes": [
        # ── Domain ──
        {
            "id": "cs",
            "name": "计算机科学",
            "node_type": "domain",
            "parent_id": None,
            "description": "计算机科学专业知识大陆",
            "position_x": 800,
            "position_y": 500,
        },
        # ══════════════════════════════════════════════════════════════════
        #  Course 1: 数据结构 (碧蓝森林)
        # ══════════════════════════════════════════════════════════════════
        {
            "id": "ds",
            "name": "数据结构",
            "node_type": "course",
            "parent_id": "cs",
            "description": "研究数据的逻辑结构、存储结构及其运算",
            "position_x": 400,
            "position_y": 480,
        },
        # Chapters
        {
            "id": "ds_ch1",
            "name": "线性表",
            "node_type": "chapter",
            "parent_id": "ds",
            "description": "顺序表与链表的基本概念和操作",
            "position_x": 310,
            "position_y": 250,
        },
        {
            "id": "ds_ch2",
            "name": "栈与队列",
            "node_type": "chapter",
            "parent_id": "ds",
            "description": "后进先出与先进先出数据结构",
            "position_x": 280,
            "position_y": 460,
        },
        {
            "id": "ds_ch3",
            "name": "树与二叉树",
            "node_type": "chapter",
            "parent_id": "ds",
            "description": "层次结构数据的表示与操作",
            "position_x": 470,
            "position_y": 560,
        },
        {
            "id": "ds_ch4",
            "name": "图",
            "node_type": "chapter",
            "parent_id": "ds",
            "description": "图的表示、遍历与应用",
            "position_x": 600,
            "position_y": 740,
        },
        # KPs: 线性表
        {
            "id": "ds_kp_array",
            "name": "顺序表",
            "node_type": "knowledge_point",
            "parent_id": "ds_ch1",
            "description": "用连续内存空间存储的线性表实现",
            "position_x": 255,
            "position_y": 205,
        },
        {
            "id": "ds_kp_linkedlist",
            "name": "链表",
            "node_type": "knowledge_point",
            "parent_id": "ds_ch1",
            "description": "用指针链接的线性表实现，包括单链表、双链表、循环链表",
            "position_x": 400,
            "position_y": 230,
        },
        {
            "id": "ds_kp_list_ops",
            "name": "线性表操作",
            "node_type": "knowledge_point",
            "parent_id": "ds_ch1",
            "description": "插入、删除、查找等基本操作及复杂度分析",
            "position_x": 330,
            "position_y": 325,
        },
        # KPs: 栈与队列
        {
            "id": "ds_kp_stack",
            "name": "栈",
            "node_type": "knowledge_point",
            "parent_id": "ds_ch2",
            "description": "后进先出(LIFO)数据结构，支持push/pop操作",
            "position_x": 215,
            "position_y": 430,
        },
        {
            "id": "ds_kp_queue",
            "name": "队列",
            "node_type": "knowledge_point",
            "parent_id": "ds_ch2",
            "description": "先进先出(FIFO)数据结构，支持enqueue/dequeue操作",
            "position_x": 370,
            "position_y": 415,
        },
        {
            "id": "ds_kp_stack_app",
            "name": "栈的应用",
            "node_type": "knowledge_point",
            "parent_id": "ds_ch2",
            "description": "表达式求值、括号匹配、递归模拟等",
            "position_x": 285,
            "position_y": 530,
        },
        # KPs: 树与二叉树
        {
            "id": "ds_kp_tree_basic",
            "name": "树的基本概念",
            "node_type": "knowledge_point",
            "parent_id": "ds_ch3",
            "description": "树的定义、术语、性质",
            "position_x": 400,
            "position_y": 560,
        },
        {
            "id": "ds_kp_binary_tree",
            "name": "二叉树",
            "node_type": "knowledge_point",
            "parent_id": "ds_ch3",
            "description": "二叉树的定义、性质、存储结构",
            "position_x": 520,
            "position_y": 510,
        },
        {
            "id": "ds_kp_tree_traversal",
            "name": "二叉树遍历",
            "node_type": "knowledge_point",
            "parent_id": "ds_ch3",
            "description": "前序、中序、后序、层序遍历算法",
            "position_x": 455,
            "position_y": 645,
        },
        {
            "id": "ds_kp_bst",
            "name": "二叉搜索树",
            "node_type": "knowledge_point",
            "parent_id": "ds_ch3",
            "description": "BST的定义、查找、插入、删除操作",
            "position_x": 590,
            "position_y": 620,
        },
        # KPs: 图
        {
            "id": "ds_kp_graph_basic",
            "name": "图的基本概念",
            "node_type": "knowledge_point",
            "parent_id": "ds_ch4",
            "description": "图的定义、术语、存储结构（邻接矩阵/邻接表）",
            "position_x": 550,
            "position_y": 730,
        },
        {
            "id": "ds_kp_graph_traversal",
            "name": "图的遍历",
            "node_type": "knowledge_point",
            "parent_id": "ds_ch4",
            "description": "BFS与DFS算法",
            "position_x": 670,
            "position_y": 705,
        },
        {
            "id": "ds_kp_shortest_path",
            "name": "最短路径",
            "node_type": "knowledge_point",
            "parent_id": "ds_ch4",
            "description": "Dijkstra算法、Floyd算法",
            "position_x": 630,
            "position_y": 810,
        },
        # ══════════════════════════════════════════════════════════════════
        #  Course 2: 计算机网络 (翡翠群岛)
        # ══════════════════════════════════════════════════════════════════
        {
            "id": "cn",
            "name": "计算机网络",
            "node_type": "course",
            "parent_id": "cs",
            "description": "研究计算机之间数据通信与网络协议",
            "position_x": 1100,
            "position_y": 480,
        },
        {
            "id": "cn_ch1",
            "name": "物理层与数据链路层",
            "node_type": "chapter",
            "parent_id": "cn",
            "description": "比特传输与帧传输的基本原理",
            "position_x": 1000,
            "position_y": 280,
        },
        {
            "id": "cn_ch2",
            "name": "网络层",
            "node_type": "chapter",
            "parent_id": "cn",
            "description": "IP协议与路由算法",
            "position_x": 1040,
            "position_y": 500,
        },
        {
            "id": "cn_ch3",
            "name": "传输层与应用层",
            "node_type": "chapter",
            "parent_id": "cn",
            "description": "端到端通信与应用协议",
            "position_x": 1100,
            "position_y": 700,
        },
        {
            "id": "cn_kp_physical",
            "name": "物理层基础",
            "node_type": "knowledge_point",
            "parent_id": "cn_ch1",
            "description": "信号编码、传输介质、信道复用",
            "position_x": 940,
            "position_y": 235,
        },
        {
            "id": "cn_kp_datalink",
            "name": "数据链路层协议",
            "node_type": "knowledge_point",
            "parent_id": "cn_ch1",
            "description": "成帧、差错控制、流量控制",
            "position_x": 1090,
            "position_y": 260,
        },
        {
            "id": "cn_kp_mac",
            "name": "MAC子层",
            "node_type": "knowledge_point",
            "parent_id": "cn_ch1",
            "description": "信道分配、CSMA/CD、以太网",
            "position_x": 1015,
            "position_y": 365,
        },
        {
            "id": "cn_kp_ip",
            "name": "IP协议",
            "node_type": "knowledge_point",
            "parent_id": "cn_ch2",
            "description": "IPv4/IPv6地址、子网划分、CIDR",
            "position_x": 960,
            "position_y": 470,
        },
        {
            "id": "cn_kp_routing",
            "name": "路由算法",
            "node_type": "knowledge_point",
            "parent_id": "cn_ch2",
            "description": "距离向量、链路状态、OSPF、BGP",
            "position_x": 1120,
            "position_y": 500,
        },
        {
            "id": "cn_kp_icmp",
            "name": "ICMP与ARP",
            "node_type": "knowledge_point",
            "parent_id": "cn_ch2",
            "description": "网络控制消息与地址解析协议",
            "position_x": 1045,
            "position_y": 580,
        },
        {
            "id": "cn_kp_tcp",
            "name": "TCP协议",
            "node_type": "knowledge_point",
            "parent_id": "cn_ch3",
            "description": "可靠传输、三次握手、流量控制、拥塞控制",
            "position_x": 990,
            "position_y": 670,
        },
        {
            "id": "cn_kp_udp",
            "name": "UDP协议",
            "node_type": "knowledge_point",
            "parent_id": "cn_ch3",
            "description": "无连接、不可靠的传输层协议",
            "position_x": 1150,
            "position_y": 660,
        },
        {
            "id": "cn_kp_http",
            "name": "HTTP与DNS",
            "node_type": "knowledge_point",
            "parent_id": "cn_ch3",
            "description": "超文本传输协议与域名系统",
            "position_x": 1100,
            "position_y": 755,
        },
        {
            "id": "cn_kp_socket",
            "name": "Socket编程",
            "node_type": "knowledge_point",
            "parent_id": "cn_ch3",
            "description": "网络编程接口、客户端/服务器模型",
            "position_x": 1260,
            "position_y": 740,
        },
        # ══════════════════════════════════════════════════════════════════
        #  Course 3: 操作系统 (紫晶山脉)
        # ══════════════════════════════════════════════════════════════════
        {
            "id": "os",
            "name": "操作系统",
            "node_type": "course",
            "parent_id": "cs",
            "description": "进程管理、内存管理、文件系统与设备管理",
            "position_x": 800,
            "position_y": 300,
        },
        {
            "id": "os_ch1",
            "name": "进程管理",
            "node_type": "chapter",
            "parent_id": "os",
            "description": "进程概念、调度、同步与死锁",
            "position_x": 350,
            "position_y": 200,
        },
        {
            "id": "os_ch2",
            "name": "内存管理",
            "node_type": "chapter",
            "parent_id": "os",
            "description": "内存分配、虚拟内存与页面置换",
            "position_x": 800,
            "position_y": 200,
        },
        {
            "id": "os_ch3",
            "name": "文件与I/O系统",
            "node_type": "chapter",
            "parent_id": "os",
            "description": "文件系统组织与输入输出管理",
            "position_x": 1200,
            "position_y": 200,
        },
        {
            "id": "os_kp_process",
            "name": "进程概念",
            "node_type": "knowledge_point",
            "parent_id": "os_ch1",
            "description": "进程定义、PCB、进程状态转换",
            "position_x": 250,
            "position_y": 180,
        },
        {
            "id": "os_kp_thread",
            "name": "线程模型",
            "node_type": "knowledge_point",
            "parent_id": "os_ch1",
            "description": "用户级线程与内核级线程",
            "position_x": 420,
            "position_y": 160,
        },
        {
            "id": "os_kp_scheduling",
            "name": "进程调度",
            "node_type": "knowledge_point",
            "parent_id": "os_ch1",
            "description": "FCFS、SJF、优先级、轮转调度算法",
            "position_x": 330,
            "position_y": 290,
        },
        {
            "id": "os_kp_sync",
            "name": "进程同步",
            "node_type": "knowledge_point",
            "parent_id": "os_ch1",
            "description": "信号量、管程、互斥锁",
            "position_x": 210,
            "position_y": 380,
        },
        {
            "id": "os_kp_deadlock",
            "name": "死锁",
            "node_type": "knowledge_point",
            "parent_id": "os_ch1",
            "description": "死锁条件、预防、避免与检测",
            "position_x": 420,
            "position_y": 410,
        },
        {
            "id": "os_kp_memory",
            "name": "内存分配",
            "node_type": "knowledge_point",
            "parent_id": "os_ch2",
            "description": "连续分配、分页、分段",
            "position_x": 680,
            "position_y": 260,
        },
        {
            "id": "os_kp_virtual",
            "name": "虚拟内存",
            "node_type": "knowledge_point",
            "parent_id": "os_ch2",
            "description": "请求分页、地址映射、TLB",
            "position_x": 830,
            "position_y": 230,
        },
        {
            "id": "os_kp_pagerep",
            "name": "页面置换",
            "node_type": "knowledge_point",
            "parent_id": "os_ch2",
            "description": "FIFO、LRU、时钟算法",
            "position_x": 760,
            "position_y": 370,
        },
        {
            "id": "os_kp_segpage",
            "name": "段页式管理",
            "node_type": "knowledge_point",
            "parent_id": "os_ch2",
            "description": "段页式地址变换与保护",
            "position_x": 920,
            "position_y": 360,
        },
        {
            "id": "os_kp_fileorg",
            "name": "文件组织",
            "node_type": "knowledge_point",
            "parent_id": "os_ch3",
            "description": "顺序文件、索引文件、散列文件",
            "position_x": 1100,
            "position_y": 230,
        },
        {
            "id": "os_kp_dir",
            "name": "目录管理",
            "node_type": "knowledge_point",
            "parent_id": "os_ch3",
            "description": "单级/多级目录、路径名",
            "position_x": 1260,
            "position_y": 210,
        },
        {
            "id": "os_kp_disk",
            "name": "磁盘调度",
            "node_type": "knowledge_point",
            "parent_id": "os_ch3",
            "description": "SCAN、C-SCAN、电梯算法",
            "position_x": 1180,
            "position_y": 340,
        },
        {
            "id": "os_kp_io",
            "name": "I/O管理",
            "node_type": "knowledge_point",
            "parent_id": "os_ch3",
            "description": "中断、DMA、缓冲技术",
            "position_x": 1350,
            "position_y": 330,
        },
        # ══════════════════════════════════════════════════════════════════
        #  Course 4: 数据库原理 (蓝钻海域)
        # ══════════════════════════════════════════════════════════════════
        {
            "id": "db",
            "name": "数据库原理",
            "node_type": "course",
            "parent_id": "cs",
            "description": "关系模型、SQL、事务处理与数据库设计",
            "position_x": 800,
            "position_y": 700,
        },
        {
            "id": "db_ch1",
            "name": "关系模型",
            "node_type": "chapter",
            "parent_id": "db",
            "description": "关系代数与关系模型基础",
            "position_x": 300,
            "position_y": 250,
        },
        {
            "id": "db_ch2",
            "name": "SQL语言",
            "node_type": "chapter",
            "parent_id": "db",
            "description": "数据定义、查询、操纵与控制",
            "position_x": 700,
            "position_y": 250,
        },
        {
            "id": "db_ch3",
            "name": "数据库设计",
            "node_type": "chapter",
            "parent_id": "db",
            "description": "ER模型与范式理论",
            "position_x": 400,
            "position_y": 550,
        },
        {
            "id": "db_ch4",
            "name": "事务处理",
            "node_type": "chapter",
            "parent_id": "db",
            "description": "事务、并发控制与恢复",
            "position_x": 900,
            "position_y": 550,
        },
        {
            "id": "db_kp_relmodel",
            "name": "关系模型",
            "node_type": "knowledge_point",
            "parent_id": "db_ch1",
            "description": "关系的数学定义、域、元组",
            "position_x": 220,
            "position_y": 200,
        },
        {
            "id": "db_kp_relalg",
            "name": "关系代数",
            "node_type": "knowledge_point",
            "parent_id": "db_ch1",
            "description": "选择、投影、连接、除法",
            "position_x": 380,
            "position_y": 220,
        },
        {
            "id": "db_kp_keys",
            "name": "键与约束",
            "node_type": "knowledge_point",
            "parent_id": "db_ch1",
            "description": "候选键、主键、外键、完整性约束",
            "position_x": 300,
            "position_y": 340,
        },
        {
            "id": "db_kp_sqlbasic",
            "name": "DDL与DML",
            "node_type": "knowledge_point",
            "parent_id": "db_ch2",
            "description": "CREATE、INSERT、UPDATE、DELETE",
            "position_x": 600,
            "position_y": 200,
        },
        {
            "id": "db_kp_join",
            "name": "连接查询",
            "node_type": "knowledge_point",
            "parent_id": "db_ch2",
            "description": "内连接、外连接、自连接",
            "position_x": 780,
            "position_y": 220,
        },
        {
            "id": "db_kp_subquery",
            "name": "子查询与视图",
            "node_type": "knowledge_point",
            "parent_id": "db_ch2",
            "description": "嵌套查询、相关子查询、视图",
            "position_x": 700,
            "position_y": 350,
        },
        {
            "id": "db_kp_index",
            "name": "索引",
            "node_type": "knowledge_point",
            "parent_id": "db_ch2",
            "description": "B+树索引、哈希索引、索引优化",
            "position_x": 880,
            "position_y": 340,
        },
        {
            "id": "db_kp_er",
            "name": "ER模型",
            "node_type": "knowledge_point",
            "parent_id": "db_ch3",
            "description": "实体、属性、联系、ER图",
            "position_x": 320,
            "position_y": 500,
        },
        {
            "id": "db_kp_normal",
            "name": "范式理论",
            "node_type": "knowledge_point",
            "parent_id": "db_ch3",
            "description": "1NF-BCNF、函数依赖、分解",
            "position_x": 470,
            "position_y": 520,
        },
        {
            "id": "db_kp_design",
            "name": "数据库设计",
            "node_type": "knowledge_point",
            "parent_id": "db_ch3",
            "description": "需求分析到物理设计全流程",
            "position_x": 400,
            "position_y": 640,
        },
        {
            "id": "db_kp_txn",
            "name": "事务概念",
            "node_type": "knowledge_point",
            "parent_id": "db_ch4",
            "description": "ACID特性、事务状态",
            "position_x": 820,
            "position_y": 500,
        },
        {
            "id": "db_kp_concur",
            "name": "并发控制",
            "node_type": "knowledge_point",
            "parent_id": "db_ch4",
            "description": "封锁协议、两阶段锁、时间戳",
            "position_x": 970,
            "position_y": 520,
        },
        {
            "id": "db_kp_recovery",
            "name": "恢复技术",
            "node_type": "knowledge_point",
            "parent_id": "db_ch4",
            "description": "日志、检查点、ARIES恢复",
            "position_x": 900,
            "position_y": 640,
        },
        # ══════════════════════════════════════════════════════════════════
        #  Course 5: 离散数学 (魔法遗迹)
        # ══════════════════════════════════════════════════════════════════
        {
            "id": "dm",
            "name": "离散数学",
            "node_type": "course",
            "parent_id": "cs",
            "description": "集合论、图论、组合数学与数理逻辑",
            "position_x": 300,
            "position_y": 200,
        },
        {
            "id": "dm_ch1",
            "name": "数理逻辑",
            "node_type": "chapter",
            "parent_id": "dm",
            "description": "命题逻辑与谓词逻辑",
            "position_x": 350,
            "position_y": 200,
        },
        {
            "id": "dm_ch2",
            "name": "集合与关系",
            "node_type": "chapter",
            "parent_id": "dm",
            "description": "集合运算、关系与函数",
            "position_x": 750,
            "position_y": 200,
        },
        {
            "id": "dm_ch3",
            "name": "图论",
            "node_type": "chapter",
            "parent_id": "dm",
            "description": "图的概念、树与着色",
            "position_x": 400,
            "position_y": 550,
        },
        {
            "id": "dm_ch4",
            "name": "组合数学",
            "node_type": "chapter",
            "parent_id": "dm",
            "description": "排列组合与递推",
            "position_x": 900,
            "position_y": 550,
        },
        {
            "id": "dm_kp_prop",
            "name": "命题逻辑",
            "node_type": "knowledge_point",
            "parent_id": "dm_ch1",
            "description": "命题、联结词、真值表、等价式",
            "position_x": 250,
            "position_y": 170,
        },
        {
            "id": "dm_kp_pred",
            "name": "谓词逻辑",
            "node_type": "knowledge_point",
            "parent_id": "dm_ch1",
            "description": "量词、谓词公式、前束范式",
            "position_x": 420,
            "position_y": 180,
        },
        {
            "id": "dm_kp_proof",
            "name": "推理方法",
            "node_type": "knowledge_point",
            "parent_id": "dm_ch1",
            "description": "自然推理、归结原理",
            "position_x": 340,
            "position_y": 300,
        },
        {
            "id": "dm_kp_sets",
            "name": "集合运算",
            "node_type": "knowledge_point",
            "parent_id": "dm_ch2",
            "description": "并、交、补、差、笛卡尔积",
            "position_x": 650,
            "position_y": 180,
        },
        {
            "id": "dm_kp_rel",
            "name": "关系",
            "node_type": "knowledge_point",
            "parent_id": "dm_ch2",
            "description": "自反、对称、传递、等价关系",
            "position_x": 820,
            "position_y": 200,
        },
        {
            "id": "dm_kp_func",
            "name": "函数",
            "node_type": "knowledge_point",
            "parent_id": "dm_ch2",
            "description": "单射、满射、双射、复合函数",
            "position_x": 740,
            "position_y": 320,
        },
        {
            "id": "dm_kp_graph",
            "name": "图的概念",
            "node_type": "knowledge_point",
            "parent_id": "dm_ch3",
            "description": "图的定义、度、路径、连通性",
            "position_x": 300,
            "position_y": 500,
        },
        {
            "id": "dm_kp_tree",
            "name": "树与生成树",
            "node_type": "knowledge_point",
            "parent_id": "dm_ch3",
            "description": "树的性质、最小生成树",
            "position_x": 450,
            "position_y": 530,
        },
        {
            "id": "dm_kp_color",
            "name": "图着色",
            "node_type": "knowledge_point",
            "parent_id": "dm_ch3",
            "description": "顶点着色、色数、四色定理",
            "position_x": 380,
            "position_y": 650,
        },
        {
            "id": "dm_kp_combo",
            "name": "排列组合",
            "node_type": "knowledge_point",
            "parent_id": "dm_ch4",
            "description": "加法原理、乘法原理、排列组合公式",
            "position_x": 800,
            "position_y": 500,
        },
        {
            "id": "dm_kp_recur",
            "name": "递推关系",
            "node_type": "knowledge_point",
            "parent_id": "dm_ch4",
            "description": "线性递推、特征方程法",
            "position_x": 960,
            "position_y": 530,
        },
        {
            "id": "dm_kp_genfun",
            "name": "生成函数",
            "node_type": "knowledge_point",
            "parent_id": "dm_ch4",
            "description": "普通生成函数与指数生成函数",
            "position_x": 880,
            "position_y": 650,
        },
        # ══════════════════════════════════════════════════════════════════
        #  Course 6: 算法设计与分析 (奇巧迷宫)
        # ══════════════════════════════════════════════════════════════════
        {
            "id": "algo",
            "name": "算法设计与分析",
            "node_type": "course",
            "parent_id": "cs",
            "description": "分治、动态规划、贪心、回溯等算法设计范式",
            "position_x": 800,
            "position_y": 500,
        },
        {
            "id": "algo_ch1",
            "name": "算法基础",
            "node_type": "chapter",
            "parent_id": "algo",
            "description": "复杂度分析与递归",
            "position_x": 350,
            "position_y": 200,
        },
        {
            "id": "algo_ch2",
            "name": "分治与动态规划",
            "node_type": "chapter",
            "parent_id": "algo",
            "description": "经典算法范式",
            "position_x": 800,
            "position_y": 300,
        },
        {
            "id": "algo_ch3",
            "name": "贪心与搜索",
            "node_type": "chapter",
            "parent_id": "algo",
            "description": "贪心策略与回溯搜索",
            "position_x": 400,
            "position_y": 550,
        },
        {
            "id": "algo_ch4",
            "name": "高级算法",
            "node_type": "chapter",
            "parent_id": "algo",
            "description": "图算法进阶与NP问题",
            "position_x": 1000,
            "position_y": 550,
        },
        {
            "id": "algo_kp_complexity",
            "name": "时间复杂度",
            "node_type": "knowledge_point",
            "parent_id": "algo_ch1",
            "description": "大O、大Omega、大Theta表示法",
            "position_x": 250,
            "position_y": 170,
        },
        {
            "id": "algo_kp_recursion",
            "name": "递归分析",
            "node_type": "knowledge_point",
            "parent_id": "algo_ch1",
            "description": "递归方程、递归树分析",
            "position_x": 420,
            "position_y": 190,
        },
        {
            "id": "algo_kp_master",
            "name": "主定理",
            "node_type": "knowledge_point",
            "parent_id": "algo_ch1",
            "description": "Master Theorem及其应用",
            "position_x": 340,
            "position_y": 310,
        },
        {
            "id": "algo_kp_divide",
            "name": "分治策略",
            "node_type": "knowledge_point",
            "parent_id": "algo_ch2",
            "description": "归并排序、快速排序、矩阵乘法",
            "position_x": 680,
            "position_y": 260,
        },
        {
            "id": "algo_kp_dp",
            "name": "动态规划",
            "node_type": "knowledge_point",
            "parent_id": "algo_ch2",
            "description": "最优子结构、重叠子问题、状态转移",
            "position_x": 850,
            "position_y": 280,
        },
        {
            "id": "algo_kp_memo",
            "name": "备忘录与表",
            "node_type": "knowledge_point",
            "parent_id": "algo_ch2",
            "description": "自顶向下与自底向上实现",
            "position_x": 770,
            "position_y": 400,
        },
        {
            "id": "algo_kp_greedy",
            "name": "贪心算法",
            "node_type": "knowledge_point",
            "parent_id": "algo_ch3",
            "description": "活动选择、哈夫曼编码、Kruskal",
            "position_x": 300,
            "position_y": 510,
        },
        {
            "id": "algo_kp_backtrack",
            "name": "回溯法",
            "node_type": "knowledge_point",
            "parent_id": "algo_ch3",
            "description": "N皇后、子集和、图着色",
            "position_x": 460,
            "position_y": 530,
        },
        {
            "id": "algo_kp_branch",
            "name": "分支限界",
            "node_type": "knowledge_point",
            "parent_id": "algo_ch3",
            "description": "BFS搜索、优先队列分支限界",
            "position_x": 380,
            "position_y": 660,
        },
        {
            "id": "algo_kp_graphadv",
            "name": "图算法进阶",
            "node_type": "knowledge_point",
            "parent_id": "algo_ch4",
            "description": "网络流、最大匹配、强连通分量",
            "position_x": 900,
            "position_y": 510,
        },
        {
            "id": "algo_kp_string",
            "name": "字符串匹配",
            "node_type": "knowledge_point",
            "parent_id": "algo_ch4",
            "description": "KMP、Rabin-Karp、AC自动机",
            "position_x": 1080,
            "position_y": 530,
        },
        {
            "id": "algo_kp_np",
            "name": "NP完全问题",
            "node_type": "knowledge_point",
            "parent_id": "algo_ch4",
            "description": "P/NP/NPC、归约、近似算法",
            "position_x": 990,
            "position_y": 660,
        },
        # ══════════════════════════════════════════════════════════════════
        #  Course 7: 编译原理 (锻造熔炉)
        # ══════════════════════════════════════════════════════════════════
        {
            "id": "compiler",
            "name": "编译原理",
            "node_type": "course",
            "parent_id": "cs",
            "description": "词法分析、语法分析、语义分析与代码生成",
            "position_x": 800,
            "position_y": 500,
        },
        {
            "id": "compiler_ch1",
            "name": "词法分析",
            "node_type": "chapter",
            "parent_id": "compiler",
            "description": "正则表达式与有限自动机",
            "position_x": 350,
            "position_y": 200,
        },
        {
            "id": "compiler_ch2",
            "name": "语法分析",
            "node_type": "chapter",
            "parent_id": "compiler",
            "description": "自顶向下与自底向上分析",
            "position_x": 800,
            "position_y": 300,
        },
        {
            "id": "compiler_ch3",
            "name": "语义与中间代码",
            "node_type": "chapter",
            "parent_id": "compiler",
            "description": "属性文法与中间代码生成",
            "position_x": 400,
            "position_y": 550,
        },
        {
            "id": "compiler_ch4",
            "name": "优化与代码生成",
            "node_type": "chapter",
            "parent_id": "compiler",
            "description": "代码优化与目标代码生成",
            "position_x": 1000,
            "position_y": 550,
        },
        {
            "id": "compiler_kp_regex",
            "name": "正则表达式",
            "node_type": "knowledge_point",
            "parent_id": "compiler_ch1",
            "description": "正则语言与正则表达式",
            "position_x": 260,
            "position_y": 180,
        },
        {
            "id": "compiler_kp_dfa",
            "name": "有限自动机",
            "node_type": "knowledge_point",
            "parent_id": "compiler_ch1",
            "description": "DFA/NFA、子集构造法",
            "position_x": 420,
            "position_y": 190,
        },
        {
            "id": "compiler_kp_lexer",
            "name": "词法分析器",
            "node_type": "knowledge_point",
            "parent_id": "compiler_ch1",
            "description": "Lex工具、Token识别",
            "position_x": 340,
            "position_y": 310,
        },
        {
            "id": "compiler_kp_cfg",
            "name": "上下文无关文法",
            "node_type": "knowledge_point",
            "parent_id": "compiler_ch2",
            "description": "CFG定义、推导、语法树",
            "position_x": 680,
            "position_y": 260,
        },
        {
            "id": "compiler_kp_ll",
            "name": "LL分析",
            "node_type": "knowledge_point",
            "parent_id": "compiler_ch2",
            "description": "FIRST/FOLLOW集、预测分析表",
            "position_x": 860,
            "position_y": 280,
        },
        {
            "id": "compiler_kp_lr",
            "name": "LR分析",
            "node_type": "knowledge_point",
            "parent_id": "compiler_ch2",
            "description": "LR(0)/SLR/LALR分析",
            "position_x": 770,
            "position_y": 400,
        },
        {
            "id": "compiler_kp_attr",
            "name": "属性文法",
            "node_type": "knowledge_point",
            "parent_id": "compiler_ch3",
            "description": "综合属性、继承属性、S-属性/L-属性",
            "position_x": 300,
            "position_y": 510,
        },
        {
            "id": "compiler_kp_ir",
            "name": "中间代码生成",
            "node_type": "knowledge_point",
            "parent_id": "compiler_ch3",
            "description": "三地址码、语法制导翻译",
            "position_x": 460,
            "position_y": 530,
        },
        {
            "id": "compiler_kp_typecheck",
            "name": "类型检查",
            "node_type": "knowledge_point",
            "parent_id": "compiler_ch3",
            "description": "类型系统、类型推断",
            "position_x": 380,
            "position_y": 660,
        },
        {
            "id": "compiler_kp_opt",
            "name": "代码优化",
            "node_type": "knowledge_point",
            "parent_id": "compiler_ch4",
            "description": "常量传播、死代码消除、循环优化",
            "position_x": 900,
            "position_y": 510,
        },
        {
            "id": "compiler_kp_codegen",
            "name": "目标代码生成",
            "node_type": "knowledge_point",
            "parent_id": "compiler_ch4",
            "description": "指令选择、寄存器分配",
            "position_x": 1080,
            "position_y": 530,
        },
        {
            "id": "compiler_kp_linker",
            "name": "链接与装载",
            "node_type": "knowledge_point",
            "parent_id": "compiler_ch4",
            "description": "符号解析、重定位、动态链接",
            "position_x": 990,
            "position_y": 660,
        },
        # ══════════════════════════════════════════════════════════════════
        #  Course 8: 软件工程 (建筑工坊)
        # ══════════════════════════════════════════════════════════════════
        {
            "id": "se",
            "name": "软件工程",
            "node_type": "course",
            "parent_id": "cs",
            "description": "需求分析、系统设计、测试与项目管理",
            "position_x": 800,
            "position_y": 500,
        },
        {
            "id": "se_ch1",
            "name": "需求与设计",
            "node_type": "chapter",
            "parent_id": "se",
            "description": "需求分析与系统设计方法",
            "position_x": 350,
            "position_y": 200,
        },
        {
            "id": "se_ch2",
            "name": "开发方法",
            "node_type": "chapter",
            "parent_id": "se",
            "description": "瀑布、敏捷与版本控制",
            "position_x": 800,
            "position_y": 300,
        },
        {
            "id": "se_ch3",
            "name": "测试与质量",
            "node_type": "chapter",
            "parent_id": "se",
            "description": "测试方法与质量保证",
            "position_x": 400,
            "position_y": 550,
        },
        {
            "id": "se_ch4",
            "name": "项目管理",
            "node_type": "chapter",
            "parent_id": "se",
            "description": "风险管理与软件维护",
            "position_x": 1000,
            "position_y": 550,
        },
        {
            "id": "se_kp_req",
            "name": "需求分析",
            "node_type": "knowledge_point",
            "parent_id": "se_ch1",
            "description": "功能需求、非功能需求、用例",
            "position_x": 250,
            "position_y": 180,
        },
        {
            "id": "se_kp_design",
            "name": "系统设计",
            "node_type": "knowledge_point",
            "parent_id": "se_ch1",
            "description": "架构设计、模块化、设计模式",
            "position_x": 420,
            "position_y": 190,
        },
        {
            "id": "se_kp_uml",
            "name": "UML建模",
            "node_type": "knowledge_point",
            "parent_id": "se_ch1",
            "description": "类图、序列图、状态图",
            "position_x": 340,
            "position_y": 310,
        },
        {
            "id": "se_kp_waterfall",
            "name": "瀑布模型",
            "node_type": "knowledge_point",
            "parent_id": "se_ch2",
            "description": "传统软件开发生命周期",
            "position_x": 680,
            "position_y": 260,
        },
        {
            "id": "se_kp_agile",
            "name": "敏捷开发",
            "node_type": "knowledge_point",
            "parent_id": "se_ch2",
            "description": "Scrum、看板、持续集成",
            "position_x": 860,
            "position_y": 280,
        },
        {
            "id": "se_kp_vcs",
            "name": "版本控制",
            "node_type": "knowledge_point",
            "parent_id": "se_ch2",
            "description": "Git工作流、分支策略",
            "position_x": 770,
            "position_y": 400,
        },
        {
            "id": "se_kp_unittest",
            "name": "单元测试",
            "node_type": "knowledge_point",
            "parent_id": "se_ch3",
            "description": "白盒测试、覆盖率、TDD",
            "position_x": 300,
            "position_y": 510,
        },
        {
            "id": "se_kp_integration",
            "name": "集成测试",
            "node_type": "knowledge_point",
            "parent_id": "se_ch3",
            "description": "自顶向下、自底向上集成",
            "position_x": 460,
            "position_y": 530,
        },
        {
            "id": "se_kp_qa",
            "name": "质量保证",
            "node_type": "knowledge_point",
            "parent_id": "se_ch3",
            "description": "代码审查、静态分析、CMMI",
            "position_x": 380,
            "position_y": 660,
        },
        {
            "id": "se_kp_risk",
            "name": "风险管理",
            "node_type": "knowledge_point",
            "parent_id": "se_ch4",
            "description": "风险识别、评估与应对",
            "position_x": 900,
            "position_y": 510,
        },
        {
            "id": "se_kp_estimate",
            "name": "项目估算",
            "node_type": "knowledge_point",
            "parent_id": "se_ch4",
            "description": "COCOMO、功能点分析",
            "position_x": 1080,
            "position_y": 530,
        },
        {
            "id": "se_kp_maintain",
            "name": "软件维护",
            "node_type": "knowledge_point",
            "parent_id": "se_ch4",
            "description": "纠错、适应、完善性维护",
            "position_x": 990,
            "position_y": 660,
        },
    ],
    "edges": [
        # ── CONTAINS (domain -> course) ──
        {"source": "cs", "target": "ds", "edge_type": "CONTAINS"},
        {"source": "cs", "target": "cn", "edge_type": "CONTAINS"},
        {"source": "cs", "target": "os", "edge_type": "CONTAINS"},
        {"source": "cs", "target": "db", "edge_type": "CONTAINS"},
        {"source": "cs", "target": "dm", "edge_type": "CONTAINS"},
        {"source": "cs", "target": "algo", "edge_type": "CONTAINS"},
        {"source": "cs", "target": "compiler", "edge_type": "CONTAINS"},
        {"source": "cs", "target": "se", "edge_type": "CONTAINS"},
        # ── CONTAINS (course -> chapter) ──
        # 数据结构
        {"source": "ds", "target": "ds_ch1", "edge_type": "CONTAINS"},
        {"source": "ds", "target": "ds_ch2", "edge_type": "CONTAINS"},
        {"source": "ds", "target": "ds_ch3", "edge_type": "CONTAINS"},
        {"source": "ds", "target": "ds_ch4", "edge_type": "CONTAINS"},
        # 计算机网络
        {"source": "cn", "target": "cn_ch1", "edge_type": "CONTAINS"},
        {"source": "cn", "target": "cn_ch2", "edge_type": "CONTAINS"},
        {"source": "cn", "target": "cn_ch3", "edge_type": "CONTAINS"},
        # 操作系统
        {"source": "os", "target": "os_ch1", "edge_type": "CONTAINS"},
        {"source": "os", "target": "os_ch2", "edge_type": "CONTAINS"},
        {"source": "os", "target": "os_ch3", "edge_type": "CONTAINS"},
        # 数据库原理
        {"source": "db", "target": "db_ch1", "edge_type": "CONTAINS"},
        {"source": "db", "target": "db_ch2", "edge_type": "CONTAINS"},
        {"source": "db", "target": "db_ch3", "edge_type": "CONTAINS"},
        {"source": "db", "target": "db_ch4", "edge_type": "CONTAINS"},
        # 离散数学
        {"source": "dm", "target": "dm_ch1", "edge_type": "CONTAINS"},
        {"source": "dm", "target": "dm_ch2", "edge_type": "CONTAINS"},
        {"source": "dm", "target": "dm_ch3", "edge_type": "CONTAINS"},
        {"source": "dm", "target": "dm_ch4", "edge_type": "CONTAINS"},
        # 算法设计
        {"source": "algo", "target": "algo_ch1", "edge_type": "CONTAINS"},
        {"source": "algo", "target": "algo_ch2", "edge_type": "CONTAINS"},
        {"source": "algo", "target": "algo_ch3", "edge_type": "CONTAINS"},
        {"source": "algo", "target": "algo_ch4", "edge_type": "CONTAINS"},
        # 编译原理
        {"source": "compiler", "target": "compiler_ch1", "edge_type": "CONTAINS"},
        {"source": "compiler", "target": "compiler_ch2", "edge_type": "CONTAINS"},
        {"source": "compiler", "target": "compiler_ch3", "edge_type": "CONTAINS"},
        {"source": "compiler", "target": "compiler_ch4", "edge_type": "CONTAINS"},
        # 软件工程
        {"source": "se", "target": "se_ch1", "edge_type": "CONTAINS"},
        {"source": "se", "target": "se_ch2", "edge_type": "CONTAINS"},
        {"source": "se", "target": "se_ch3", "edge_type": "CONTAINS"},
        {"source": "se", "target": "se_ch4", "edge_type": "CONTAINS"},
        # ── CONTAINS (chapter -> knowledge_point) ──
        # 数据结构
        {"source": "ds_ch1", "target": "ds_kp_array", "edge_type": "CONTAINS"},
        {"source": "ds_ch1", "target": "ds_kp_linkedlist", "edge_type": "CONTAINS"},
        {"source": "ds_ch1", "target": "ds_kp_list_ops", "edge_type": "CONTAINS"},
        {"source": "ds_ch2", "target": "ds_kp_stack", "edge_type": "CONTAINS"},
        {"source": "ds_ch2", "target": "ds_kp_queue", "edge_type": "CONTAINS"},
        {"source": "ds_ch2", "target": "ds_kp_stack_app", "edge_type": "CONTAINS"},
        {"source": "ds_ch3", "target": "ds_kp_tree_basic", "edge_type": "CONTAINS"},
        {"source": "ds_ch3", "target": "ds_kp_binary_tree", "edge_type": "CONTAINS"},
        {"source": "ds_ch3", "target": "ds_kp_tree_traversal", "edge_type": "CONTAINS"},
        {"source": "ds_ch3", "target": "ds_kp_bst", "edge_type": "CONTAINS"},
        {"source": "ds_ch4", "target": "ds_kp_graph_basic", "edge_type": "CONTAINS"},
        {
            "source": "ds_ch4",
            "target": "ds_kp_graph_traversal",
            "edge_type": "CONTAINS",
        },
        {"source": "ds_ch4", "target": "ds_kp_shortest_path", "edge_type": "CONTAINS"},
        # 计算机网络
        {"source": "cn_ch1", "target": "cn_kp_physical", "edge_type": "CONTAINS"},
        {"source": "cn_ch1", "target": "cn_kp_datalink", "edge_type": "CONTAINS"},
        {"source": "cn_ch1", "target": "cn_kp_mac", "edge_type": "CONTAINS"},
        {"source": "cn_ch2", "target": "cn_kp_ip", "edge_type": "CONTAINS"},
        {"source": "cn_ch2", "target": "cn_kp_routing", "edge_type": "CONTAINS"},
        {"source": "cn_ch2", "target": "cn_kp_icmp", "edge_type": "CONTAINS"},
        {"source": "cn_ch3", "target": "cn_kp_tcp", "edge_type": "CONTAINS"},
        {"source": "cn_ch3", "target": "cn_kp_udp", "edge_type": "CONTAINS"},
        {"source": "cn_ch3", "target": "cn_kp_http", "edge_type": "CONTAINS"},
        {"source": "cn_ch3", "target": "cn_kp_socket", "edge_type": "CONTAINS"},
        # 操作系统
        {"source": "os_ch1", "target": "os_kp_process", "edge_type": "CONTAINS"},
        {"source": "os_ch1", "target": "os_kp_thread", "edge_type": "CONTAINS"},
        {"source": "os_ch1", "target": "os_kp_scheduling", "edge_type": "CONTAINS"},
        {"source": "os_ch1", "target": "os_kp_sync", "edge_type": "CONTAINS"},
        {"source": "os_ch1", "target": "os_kp_deadlock", "edge_type": "CONTAINS"},
        {"source": "os_ch2", "target": "os_kp_memory", "edge_type": "CONTAINS"},
        {"source": "os_ch2", "target": "os_kp_virtual", "edge_type": "CONTAINS"},
        {"source": "os_ch2", "target": "os_kp_pagerep", "edge_type": "CONTAINS"},
        {"source": "os_ch2", "target": "os_kp_segpage", "edge_type": "CONTAINS"},
        {"source": "os_ch3", "target": "os_kp_fileorg", "edge_type": "CONTAINS"},
        {"source": "os_ch3", "target": "os_kp_dir", "edge_type": "CONTAINS"},
        {"source": "os_ch3", "target": "os_kp_disk", "edge_type": "CONTAINS"},
        {"source": "os_ch3", "target": "os_kp_io", "edge_type": "CONTAINS"},
        # 数据库原理
        {"source": "db_ch1", "target": "db_kp_relmodel", "edge_type": "CONTAINS"},
        {"source": "db_ch1", "target": "db_kp_relalg", "edge_type": "CONTAINS"},
        {"source": "db_ch1", "target": "db_kp_keys", "edge_type": "CONTAINS"},
        {"source": "db_ch2", "target": "db_kp_sqlbasic", "edge_type": "CONTAINS"},
        {"source": "db_ch2", "target": "db_kp_join", "edge_type": "CONTAINS"},
        {"source": "db_ch2", "target": "db_kp_subquery", "edge_type": "CONTAINS"},
        {"source": "db_ch2", "target": "db_kp_index", "edge_type": "CONTAINS"},
        {"source": "db_ch3", "target": "db_kp_er", "edge_type": "CONTAINS"},
        {"source": "db_ch3", "target": "db_kp_normal", "edge_type": "CONTAINS"},
        {"source": "db_ch3", "target": "db_kp_design", "edge_type": "CONTAINS"},
        {"source": "db_ch4", "target": "db_kp_txn", "edge_type": "CONTAINS"},
        {"source": "db_ch4", "target": "db_kp_concur", "edge_type": "CONTAINS"},
        {"source": "db_ch4", "target": "db_kp_recovery", "edge_type": "CONTAINS"},
        # 离散数学
        {"source": "dm_ch1", "target": "dm_kp_prop", "edge_type": "CONTAINS"},
        {"source": "dm_ch1", "target": "dm_kp_pred", "edge_type": "CONTAINS"},
        {"source": "dm_ch1", "target": "dm_kp_proof", "edge_type": "CONTAINS"},
        {"source": "dm_ch2", "target": "dm_kp_sets", "edge_type": "CONTAINS"},
        {"source": "dm_ch2", "target": "dm_kp_rel", "edge_type": "CONTAINS"},
        {"source": "dm_ch2", "target": "dm_kp_func", "edge_type": "CONTAINS"},
        {"source": "dm_ch3", "target": "dm_kp_graph", "edge_type": "CONTAINS"},
        {"source": "dm_ch3", "target": "dm_kp_tree", "edge_type": "CONTAINS"},
        {"source": "dm_ch3", "target": "dm_kp_color", "edge_type": "CONTAINS"},
        {"source": "dm_ch4", "target": "dm_kp_combo", "edge_type": "CONTAINS"},
        {"source": "dm_ch4", "target": "dm_kp_recur", "edge_type": "CONTAINS"},
        {"source": "dm_ch4", "target": "dm_kp_genfun", "edge_type": "CONTAINS"},
        # 算法设计
        {"source": "algo_ch1", "target": "algo_kp_complexity", "edge_type": "CONTAINS"},
        {"source": "algo_ch1", "target": "algo_kp_recursion", "edge_type": "CONTAINS"},
        {"source": "algo_ch1", "target": "algo_kp_master", "edge_type": "CONTAINS"},
        {"source": "algo_ch2", "target": "algo_kp_divide", "edge_type": "CONTAINS"},
        {"source": "algo_ch2", "target": "algo_kp_dp", "edge_type": "CONTAINS"},
        {"source": "algo_ch2", "target": "algo_kp_memo", "edge_type": "CONTAINS"},
        {"source": "algo_ch3", "target": "algo_kp_greedy", "edge_type": "CONTAINS"},
        {"source": "algo_ch3", "target": "algo_kp_backtrack", "edge_type": "CONTAINS"},
        {"source": "algo_ch3", "target": "algo_kp_branch", "edge_type": "CONTAINS"},
        {"source": "algo_ch4", "target": "algo_kp_graphadv", "edge_type": "CONTAINS"},
        {"source": "algo_ch4", "target": "algo_kp_string", "edge_type": "CONTAINS"},
        {"source": "algo_ch4", "target": "algo_kp_np", "edge_type": "CONTAINS"},
        # 编译原理
        {
            "source": "compiler_ch1",
            "target": "compiler_kp_regex",
            "edge_type": "CONTAINS",
        },
        {
            "source": "compiler_ch1",
            "target": "compiler_kp_dfa",
            "edge_type": "CONTAINS",
        },
        {
            "source": "compiler_ch1",
            "target": "compiler_kp_lexer",
            "edge_type": "CONTAINS",
        },
        {
            "source": "compiler_ch2",
            "target": "compiler_kp_cfg",
            "edge_type": "CONTAINS",
        },
        {"source": "compiler_ch2", "target": "compiler_kp_ll", "edge_type": "CONTAINS"},
        {"source": "compiler_ch2", "target": "compiler_kp_lr", "edge_type": "CONTAINS"},
        {
            "source": "compiler_ch3",
            "target": "compiler_kp_attr",
            "edge_type": "CONTAINS",
        },
        {"source": "compiler_ch3", "target": "compiler_kp_ir", "edge_type": "CONTAINS"},
        {
            "source": "compiler_ch3",
            "target": "compiler_kp_typecheck",
            "edge_type": "CONTAINS",
        },
        {
            "source": "compiler_ch4",
            "target": "compiler_kp_opt",
            "edge_type": "CONTAINS",
        },
        {
            "source": "compiler_ch4",
            "target": "compiler_kp_codegen",
            "edge_type": "CONTAINS",
        },
        {
            "source": "compiler_ch4",
            "target": "compiler_kp_linker",
            "edge_type": "CONTAINS",
        },
        # 软件工程
        {"source": "se_ch1", "target": "se_kp_req", "edge_type": "CONTAINS"},
        {"source": "se_ch1", "target": "se_kp_design", "edge_type": "CONTAINS"},
        {"source": "se_ch1", "target": "se_kp_uml", "edge_type": "CONTAINS"},
        {"source": "se_ch2", "target": "se_kp_waterfall", "edge_type": "CONTAINS"},
        {"source": "se_ch2", "target": "se_kp_agile", "edge_type": "CONTAINS"},
        {"source": "se_ch2", "target": "se_kp_vcs", "edge_type": "CONTAINS"},
        {"source": "se_ch3", "target": "se_kp_unittest", "edge_type": "CONTAINS"},
        {"source": "se_ch3", "target": "se_kp_integration", "edge_type": "CONTAINS"},
        {"source": "se_ch3", "target": "se_kp_qa", "edge_type": "CONTAINS"},
        {"source": "se_ch4", "target": "se_kp_risk", "edge_type": "CONTAINS"},
        {"source": "se_ch4", "target": "se_kp_estimate", "edge_type": "CONTAINS"},
        {"source": "se_ch4", "target": "se_kp_maintain", "edge_type": "CONTAINS"},
        # ══════════════════════════════════════════════════════════════════
        #  PREREQUISITE edges (within courses)
        # ══════════════════════════════════════════════════════════════════
        # 数据结构 chapter-level
        {"source": "ds_ch1", "target": "ds_ch2", "edge_type": "PREREQUISITE"},
        {"source": "ds_ch2", "target": "ds_ch3", "edge_type": "PREREQUISITE"},
        {"source": "ds_ch3", "target": "ds_ch4", "edge_type": "PREREQUISITE"},
        # 数据结构 KP-level
        {
            "source": "ds_kp_array",
            "target": "ds_kp_linkedlist",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "ds_kp_array",
            "target": "ds_kp_list_ops",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "ds_kp_linkedlist",
            "target": "ds_kp_list_ops",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "ds_kp_list_ops",
            "target": "ds_kp_stack",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "ds_kp_list_ops",
            "target": "ds_kp_queue",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "ds_kp_stack",
            "target": "ds_kp_stack_app",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "ds_kp_stack_app",
            "target": "ds_kp_tree_basic",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "ds_kp_queue",
            "target": "ds_kp_tree_basic",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "ds_kp_tree_basic",
            "target": "ds_kp_binary_tree",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "ds_kp_binary_tree",
            "target": "ds_kp_tree_traversal",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "ds_kp_binary_tree",
            "target": "ds_kp_bst",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "ds_kp_bst",
            "target": "ds_kp_graph_basic",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "ds_kp_graph_basic",
            "target": "ds_kp_graph_traversal",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "ds_kp_graph_traversal",
            "target": "ds_kp_shortest_path",
            "edge_type": "PREREQUISITE",
        },
        # 计算机网络 chapter-level
        {"source": "cn_ch1", "target": "cn_ch2", "edge_type": "PREREQUISITE"},
        {"source": "cn_ch2", "target": "cn_ch3", "edge_type": "PREREQUISITE"},
        # 计算机网络 KP-level
        {
            "source": "cn_kp_physical",
            "target": "cn_kp_datalink",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "cn_kp_datalink",
            "target": "cn_kp_mac",
            "edge_type": "PREREQUISITE",
        },
        {"source": "cn_kp_mac", "target": "cn_kp_ip", "edge_type": "PREREQUISITE"},
        {"source": "cn_kp_ip", "target": "cn_kp_routing", "edge_type": "PREREQUISITE"},
        {"source": "cn_kp_ip", "target": "cn_kp_icmp", "edge_type": "PREREQUISITE"},
        {"source": "cn_kp_routing", "target": "cn_kp_tcp", "edge_type": "PREREQUISITE"},
        {"source": "cn_kp_icmp", "target": "cn_kp_tcp", "edge_type": "PREREQUISITE"},
        {"source": "cn_kp_tcp", "target": "cn_kp_udp", "edge_type": "PREREQUISITE"},
        {"source": "cn_kp_tcp", "target": "cn_kp_http", "edge_type": "PREREQUISITE"},
        {"source": "cn_kp_http", "target": "cn_kp_socket", "edge_type": "PREREQUISITE"},
        # 操作系统
        {"source": "os_ch1", "target": "os_ch2", "edge_type": "PREREQUISITE"},
        {"source": "os_ch2", "target": "os_ch3", "edge_type": "PREREQUISITE"},
        {
            "source": "os_kp_process",
            "target": "os_kp_thread",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "os_kp_thread",
            "target": "os_kp_scheduling",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "os_kp_scheduling",
            "target": "os_kp_sync",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "os_kp_sync",
            "target": "os_kp_deadlock",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "os_kp_deadlock",
            "target": "os_kp_memory",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "os_kp_memory",
            "target": "os_kp_virtual",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "os_kp_virtual",
            "target": "os_kp_pagerep",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "os_kp_virtual",
            "target": "os_kp_segpage",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "os_kp_segpage",
            "target": "os_kp_fileorg",
            "edge_type": "PREREQUISITE",
        },
        {"source": "os_kp_fileorg", "target": "os_kp_dir", "edge_type": "PREREQUISITE"},
        {"source": "os_kp_dir", "target": "os_kp_disk", "edge_type": "PREREQUISITE"},
        {"source": "os_kp_disk", "target": "os_kp_io", "edge_type": "PREREQUISITE"},
        # 数据库原理
        {"source": "db_ch1", "target": "db_ch2", "edge_type": "PREREQUISITE"},
        {"source": "db_ch2", "target": "db_ch3", "edge_type": "PREREQUISITE"},
        {"source": "db_ch2", "target": "db_ch4", "edge_type": "PREREQUISITE"},
        {
            "source": "db_kp_relmodel",
            "target": "db_kp_relalg",
            "edge_type": "PREREQUISITE",
        },
        {"source": "db_kp_relalg", "target": "db_kp_keys", "edge_type": "PREREQUISITE"},
        {
            "source": "db_kp_keys",
            "target": "db_kp_sqlbasic",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "db_kp_sqlbasic",
            "target": "db_kp_join",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "db_kp_join",
            "target": "db_kp_subquery",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "db_kp_subquery",
            "target": "db_kp_index",
            "edge_type": "PREREQUISITE",
        },
        {"source": "db_kp_index", "target": "db_kp_er", "edge_type": "PREREQUISITE"},
        {"source": "db_kp_er", "target": "db_kp_normal", "edge_type": "PREREQUISITE"},
        {
            "source": "db_kp_normal",
            "target": "db_kp_design",
            "edge_type": "PREREQUISITE",
        },
        {"source": "db_kp_index", "target": "db_kp_txn", "edge_type": "PREREQUISITE"},
        {"source": "db_kp_txn", "target": "db_kp_concur", "edge_type": "PREREQUISITE"},
        {
            "source": "db_kp_concur",
            "target": "db_kp_recovery",
            "edge_type": "PREREQUISITE",
        },
        # 离散数学
        {"source": "dm_ch1", "target": "dm_ch2", "edge_type": "PREREQUISITE"},
        {"source": "dm_ch2", "target": "dm_ch3", "edge_type": "PREREQUISITE"},
        {"source": "dm_ch2", "target": "dm_ch4", "edge_type": "PREREQUISITE"},
        {"source": "dm_kp_prop", "target": "dm_kp_pred", "edge_type": "PREREQUISITE"},
        {"source": "dm_kp_pred", "target": "dm_kp_proof", "edge_type": "PREREQUISITE"},
        {"source": "dm_kp_proof", "target": "dm_kp_sets", "edge_type": "PREREQUISITE"},
        {"source": "dm_kp_sets", "target": "dm_kp_rel", "edge_type": "PREREQUISITE"},
        {"source": "dm_kp_rel", "target": "dm_kp_func", "edge_type": "PREREQUISITE"},
        {"source": "dm_kp_func", "target": "dm_kp_graph", "edge_type": "PREREQUISITE"},
        {"source": "dm_kp_graph", "target": "dm_kp_tree", "edge_type": "PREREQUISITE"},
        {"source": "dm_kp_tree", "target": "dm_kp_color", "edge_type": "PREREQUISITE"},
        {"source": "dm_kp_func", "target": "dm_kp_combo", "edge_type": "PREREQUISITE"},
        {"source": "dm_kp_combo", "target": "dm_kp_recur", "edge_type": "PREREQUISITE"},
        {
            "source": "dm_kp_recur",
            "target": "dm_kp_genfun",
            "edge_type": "PREREQUISITE",
        },
        # 算法设计
        {"source": "algo_ch1", "target": "algo_ch2", "edge_type": "PREREQUISITE"},
        {"source": "algo_ch2", "target": "algo_ch3", "edge_type": "PREREQUISITE"},
        {"source": "algo_ch2", "target": "algo_ch4", "edge_type": "PREREQUISITE"},
        {
            "source": "algo_kp_complexity",
            "target": "algo_kp_recursion",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "algo_kp_recursion",
            "target": "algo_kp_master",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "algo_kp_master",
            "target": "algo_kp_divide",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "algo_kp_divide",
            "target": "algo_kp_dp",
            "edge_type": "PREREQUISITE",
        },
        {"source": "algo_kp_dp", "target": "algo_kp_memo", "edge_type": "PREREQUISITE"},
        {
            "source": "algo_kp_memo",
            "target": "algo_kp_greedy",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "algo_kp_greedy",
            "target": "algo_kp_backtrack",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "algo_kp_backtrack",
            "target": "algo_kp_branch",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "algo_kp_memo",
            "target": "algo_kp_graphadv",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "algo_kp_graphadv",
            "target": "algo_kp_string",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "algo_kp_string",
            "target": "algo_kp_np",
            "edge_type": "PREREQUISITE",
        },
        # 编译原理
        {
            "source": "compiler_ch1",
            "target": "compiler_ch2",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "compiler_ch2",
            "target": "compiler_ch3",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "compiler_ch3",
            "target": "compiler_ch4",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "compiler_kp_regex",
            "target": "compiler_kp_dfa",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "compiler_kp_dfa",
            "target": "compiler_kp_lexer",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "compiler_kp_lexer",
            "target": "compiler_kp_cfg",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "compiler_kp_cfg",
            "target": "compiler_kp_ll",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "compiler_kp_ll",
            "target": "compiler_kp_lr",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "compiler_kp_lr",
            "target": "compiler_kp_attr",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "compiler_kp_attr",
            "target": "compiler_kp_ir",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "compiler_kp_ir",
            "target": "compiler_kp_typecheck",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "compiler_kp_typecheck",
            "target": "compiler_kp_opt",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "compiler_kp_opt",
            "target": "compiler_kp_codegen",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "compiler_kp_codegen",
            "target": "compiler_kp_linker",
            "edge_type": "PREREQUISITE",
        },
        # 软件工程
        {"source": "se_ch1", "target": "se_ch2", "edge_type": "PREREQUISITE"},
        {"source": "se_ch2", "target": "se_ch3", "edge_type": "PREREQUISITE"},
        {"source": "se_ch2", "target": "se_ch4", "edge_type": "PREREQUISITE"},
        {"source": "se_kp_req", "target": "se_kp_design", "edge_type": "PREREQUISITE"},
        {"source": "se_kp_design", "target": "se_kp_uml", "edge_type": "PREREQUISITE"},
        {
            "source": "se_kp_uml",
            "target": "se_kp_waterfall",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "se_kp_waterfall",
            "target": "se_kp_agile",
            "edge_type": "PREREQUISITE",
        },
        {"source": "se_kp_agile", "target": "se_kp_vcs", "edge_type": "PREREQUISITE"},
        {
            "source": "se_kp_vcs",
            "target": "se_kp_unittest",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "se_kp_unittest",
            "target": "se_kp_integration",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "se_kp_integration",
            "target": "se_kp_qa",
            "edge_type": "PREREQUISITE",
        },
        {"source": "se_kp_vcs", "target": "se_kp_risk", "edge_type": "PREREQUISITE"},
        {
            "source": "se_kp_risk",
            "target": "se_kp_estimate",
            "edge_type": "PREREQUISITE",
        },
        {
            "source": "se_kp_estimate",
            "target": "se_kp_maintain",
            "edge_type": "PREREQUISITE",
        },
        # ══════════════════════════════════════════════════════════════════
        #  RELATED_TO (cross-course tunnels / 暗道)
        # ══════════════════════════════════════════════════════════════════
        # 数据结构 <-> 计算机网络
        {
            "source": "ds_kp_graph_traversal",
            "target": "cn_kp_routing",
            "edge_type": "RELATED_TO",
        },
        {
            "source": "ds_kp_graph_basic",
            "target": "cn_kp_ip",
            "edge_type": "RELATED_TO",
        },
        {"source": "ds_kp_queue", "target": "cn_kp_tcp", "edge_type": "RELATED_TO"},
        {
            "source": "ds_kp_stack_app",
            "target": "cn_kp_http",
            "edge_type": "RELATED_TO",
        },
        {
            "source": "ds_kp_tree_traversal",
            "target": "cn_kp_routing",
            "edge_type": "RELATED_TO",
        },
        # 数据结构 <-> 操作系统
        {
            "source": "ds_kp_queue",
            "target": "os_kp_scheduling",
            "edge_type": "RELATED_TO",
        },
        {
            "source": "ds_kp_linkedlist",
            "target": "os_kp_memory",
            "edge_type": "RELATED_TO",
        },
        # 数据结构 <-> 数据库
        {"source": "ds_kp_bst", "target": "db_kp_index", "edge_type": "RELATED_TO"},
        {
            "source": "ds_kp_graph_basic",
            "target": "db_kp_relalg",
            "edge_type": "RELATED_TO",
        },
        # 离散数学 <-> 算法
        {
            "source": "dm_kp_graph",
            "target": "algo_kp_graphadv",
            "edge_type": "RELATED_TO",
        },
        {"source": "dm_kp_combo", "target": "algo_kp_dp", "edge_type": "RELATED_TO"},
        {
            "source": "dm_kp_recur",
            "target": "algo_kp_recursion",
            "edge_type": "RELATED_TO",
        },
        # 离散数学 <-> 编译原理
        {
            "source": "dm_kp_prop",
            "target": "compiler_kp_regex",
            "edge_type": "RELATED_TO",
        },
        {
            "source": "dm_kp_graph",
            "target": "compiler_kp_dfa",
            "edge_type": "RELATED_TO",
        },
        # 操作系统 <-> 计算机网络
        {"source": "os_kp_sync", "target": "cn_kp_tcp", "edge_type": "RELATED_TO"},
        {"source": "os_kp_io", "target": "cn_kp_socket", "edge_type": "RELATED_TO"},
        # 数据库 <-> 操作系统
        {"source": "db_kp_concur", "target": "os_kp_sync", "edge_type": "RELATED_TO"},
        {"source": "db_kp_recovery", "target": "os_kp_disk", "edge_type": "RELATED_TO"},
        # 软件工程 <-> 数据库
        {"source": "se_kp_design", "target": "db_kp_er", "edge_type": "RELATED_TO"},
    ],
}


# ---------------------------------------------------------------------------
# Build the graph once on import
# ---------------------------------------------------------------------------

_graph: nx.DiGraph = nx.DiGraph()


def _build_graph() -> None:
    """Populate the module-level DiGraph from SEED_DATA."""
    for node in SEED_DATA["nodes"]:
        _graph.add_node(
            node["id"],
            name=node["name"],
            node_type=node["node_type"],
            parent_id=node["parent_id"],
            description=node["description"],
            position_x=node["position_x"],
            position_y=node["position_y"],
        )
    for edge in SEED_DATA["edges"]:
        _graph.add_edge(
            edge["source"],
            edge["target"],
            edge_type=edge["edge_type"],
        )


_build_graph()


# ---------------------------------------------------------------------------
# Public query API
# ---------------------------------------------------------------------------


def get_node(node_id: str) -> Optional[Dict]:
    """Return a single node dict, or None if not found."""
    if node_id not in _graph:
        return None
    attrs = dict(_graph.nodes[node_id])
    attrs["id"] = node_id
    return attrs


def get_all_domains() -> List[Dict]:
    """Return all domain-type nodes."""
    result = []
    for nid, attrs in _graph.nodes(data=True):
        if attrs.get("node_type") == "domain":
            d = dict(attrs)
            d["id"] = nid
            result.append(d)
    return result


def get_domain_map(domain_id: str) -> Dict:
    """Return all nodes and edges belonging to a domain, suitable for map rendering."""
    descendants = set()

    def _collect(parent_id: str) -> None:
        descendants.add(parent_id)
        for _, target, data in _graph.out_edges(parent_id, data=True):
            if data.get("edge_type") == "CONTAINS":
                _collect(target)

    _collect(domain_id)

    nodes = []
    for nid in descendants:
        attrs = dict(_graph.nodes[nid])
        attrs["id"] = nid
        nodes.append(attrs)

    edges = []
    for src, tgt, data in _graph.edges(data=True):
        if src in descendants or tgt in descendants:
            edges.append({"source": src, "target": tgt, "edge_type": data["edge_type"]})

    return {"domain_id": domain_id, "nodes": nodes, "edges": edges}


def get_prerequisites(node_id: str) -> List[str]:
    """Return node IDs that are PREREQUISITE predecessors of node_id."""
    result = []
    for src, _, data in _graph.in_edges(node_id, data=True):
        if data.get("edge_type") == "PREREQUISITE":
            result.append(src)
    return result


def get_successors(node_id: str) -> List[str]:
    """Return node IDs that node_id is a PREREQUISITE for."""
    result = []
    for _, tgt, data in _graph.out_edges(node_id, data=True):
        if data.get("edge_type") == "PREREQUISITE":
            result.append(tgt)
    return result


def get_related_nodes(node_id: str) -> List[str]:
    """Return node IDs connected via RELATED_TO edges (bidirectional tunnels)."""
    result = []
    for _, tgt, data in _graph.out_edges(node_id, data=True):
        if data.get("edge_type") == "RELATED_TO":
            result.append(tgt)
    for src, _, data in _graph.in_edges(node_id, data=True):
        if data.get("edge_type") == "RELATED_TO":
            result.append(src)
    return result


def get_entry_nodes(domain_id: str) -> List[str]:
    """Return knowledge-point nodes with no PREREQUISITE predecessors (starting points)."""
    domain_map = get_domain_map(domain_id)
    domain_node_ids = {n["id"] for n in domain_map["nodes"]}

    entry = []
    for nid in domain_node_ids:
        attrs = _graph.nodes[nid]
        if attrs.get("node_type") != "knowledge_point":
            continue
        prereqs = get_prerequisites(nid)
        has_prereq = any(
            p in domain_node_ids
            and _graph.nodes[p].get("node_type") == "knowledge_point"
            for p in prereqs
        )
        if not has_prereq:
            entry.append(nid)
    return entry


def count_nodes_in_domain(domain_id: str) -> int:
    """Count knowledge_point nodes in a domain."""
    domain_map = get_domain_map(domain_id)
    return sum(1 for n in domain_map["nodes"] if n["node_type"] == "knowledge_point")


def get_all_knowledge_points_in_domain(domain_id: str) -> List[str]:
    """Return all knowledge_point node IDs in a domain."""
    domain_map = get_domain_map(domain_id)
    return [n["id"] for n in domain_map["nodes"] if n["node_type"] == "knowledge_point"]


def get_domain_for_node(node_id: str) -> Optional[str]:
    """Walk up CONTAINS edges to find the domain a node belongs to."""
    current = node_id
    visited = set()
    while current and current not in visited:
        visited.add(current)
        attrs = _graph.nodes.get(current)
        if attrs is None:
            return None
        if attrs.get("node_type") == "domain":
            return current
        parent = attrs.get("parent_id")
        if parent is None:
            return None
        current = parent
    return None
