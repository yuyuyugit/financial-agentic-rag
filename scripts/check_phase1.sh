#!/bin/bash

echo "========================================="
echo "Phase 1 验证检查"
echo "========================================="

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

PASS=0
FAIL=0

# 1. 文件检查
echo -e "\n📁 1. 文件结构检查"

check_file() {
    if [ -f "$1" ]; then
        echo -e "   ${GREEN}✓${NC} $1"
        ((PASS++))
    else
        echo -e "   ${RED}✗${NC} $1 不存在"
        ((FAIL++))
    fi
}

check_file "src/router/intent_router.py"
check_file "src/router/__init__.py"
check_file "src/retrieval/keyword_search.py"
check_file "src/retrieval/__init__.py"
check_file "src/config/router_config.yaml"
check_file "src/config/keyword_search_config.yaml"

# 2. Python 导入检查
echo -e "\n🐍 2. Python 导入检查"

python3 << 'EOF'
import sys
sys.path.insert(0, '.')

try:
    from src.router import IntentRouter, QueryType
    print("   ✓ IntentRouter 和 QueryType 导入成功")
    sys.exit(0)
except Exception as e:
    print(f"   ✗ 导入失败: {e}")
    sys.exit(1)
EOF

if [ $? -eq 0 ]; then
    ((PASS++))
else
    ((FAIL++))
fi

python3 << 'EOF'
import sys
sys.path.insert(0, '.')

try:
    from src.retrieval import KeywordSearcher
    print("   ✓ KeywordSearcher 导入成功")
    sys.exit(0)
except Exception as e:
    print(f"   ✗ 导入失败: {e}")
    sys.exit(1)
EOF

if [ $? -eq 0 ]; then
    ((PASS++))
else
    ((FAIL++))
fi

# 3. QueryType 枚举检查
echo -e "\n📋 3. QueryType 枚举检查"

python3 << 'EOF'
import sys
sys.path.insert(0, '.')

from src.router import QueryType

if hasattr(QueryType, 'SIMPLE') and hasattr(QueryType, 'COMPLEX'):
    print("   ✓ QueryType 包含 SIMPLE 和 COMPLEX")
    sys.exit(0)
else:
    print("   ✗ QueryType 缺少必要的枚举值")
    sys.exit(1)
EOF

if [ $? -eq 0 ]; then
    ((PASS++))
else
    ((FAIL++))
fi


# 4. IntentRouter 关键词路由检查
echo -e "\n🛣️  4. IntentRouter 关键词路由检查"

python3 << 'EOF'
import sys
sys.path.insert(0, '.')

from src.router import IntentRouter, QueryType

router = IntentRouter()

# Test keyword matching
test_queries = [
    ("我的资产是多少", QueryType.SIMPLE),
    ("查看持仓", QueryType.SIMPLE),
    ("账户余额", QueryType.SIMPLE),
]

all_passed = True
for query, expected in test_queries:
    result = router.route(query)
    if result == expected:
        print(f"   ✓ '{query}' -> {result.value}")
    else:
        print(f"   ✗ '{query}' -> {result.value} (期望: {expected.value})")
        all_passed = False

sys.exit(0 if all_passed else 1)
EOF

if [ $? -eq 0 ]; then
    ((PASS++))
else
    ((FAIL++))
fi

# 5. KeywordSearcher 检查
echo -e "\n🔍 5. KeywordSearcher 检查"

python3 << 'EOF'
import sys
sys.path.insert(0, '.')

from src.retrieval import KeywordSearcher

searcher = KeywordSearcher()

# Test search method
test_cases = [
    ("我的资产", "您的总资产为 ¥1,234,567.89"),
    ("持仓", "当前持仓：茅台(600519) 100股，腾讯(0700.HK) 200股"),
    ("余额", "可用余额：¥50,000.00"),
    ("不存在的查询", "未找到相关信息"),
]

all_passed = True
for query, expected_result in test_cases:
    result = searcher.search(query)
    if result["result"] == expected_result and result["source"] == "keyword_search":
        print(f"   ✓ 搜索 '{query}' 成功")
    else:
        print(f"   ✗ 搜索 '{query}' 失败")
        print(f"      期望: {expected_result}")
        print(f"      实际: {result['result']}")
        all_passed = False

sys.exit(0 if all_passed else 1)
EOF

if [ $? -eq 0 ]; then
    ((PASS++))
else
    ((FAIL++))
fi

# 7. 总结
echo -e "\n========================================="
echo -e "检查结果: ${GREEN}通过 $PASS${NC} / 共 $((PASS+FAIL)) 项"
echo "========================================="

