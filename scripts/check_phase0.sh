#!/bin/bash

echo "========================================="
echo "Phase 0 验证检查"
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

check_file "Dockerfile"
check_file "docker-compose.yml"
check_file "requirements.txt"
check_file "src/api/main.py"

# 2. 环境变量检查
echo -e "\n🔑 2. 环境变量检查"
if [ -f ".env" ]; then
    echo -e "   ${GREEN}✓${NC} .env 文件存在"
    ((PASS++))
else
    echo -e "   ${RED}✗${NC} .env 文件不存在"
    ((FAIL++))
fi

# 3. Docker 容器检查
echo -e "\n🐳 3. Docker 容器检查"
RUNNING_CONTAINERS=$(docker ps --format "table {{.Names}}" | tail -n +2 | wc -l | tr -d ' ')
echo "   运行中的容器数: $RUNNING_CONTAINERS"

if docker ps --format "table {{.Names}}" | grep -q "backend"; then
    echo -e "   ${GREEN}✓${NC} Backend 容器运行中"
    ((PASS++))
else
    echo -e "   ${YELLOW}⚠${NC} Backend 容器未运行"
fi

if docker ps --format "table {{.Names}}" | grep -q "weaviate"; then
    echo -e "   ${GREEN}✓${NC} Weaviate 容器运行中"
    ((PASS++))
else
    echo -e "   ${YELLOW}⚠${NC} Weaviate 容器未运行"
fi

if docker ps --format "table {{.Names}}" | grep -q "frontend"; then
    echo -e "   ${GREEN}✓${NC} Frontend 容器运行中"
    ((PASS++))
else
    echo -e "   ${YELLOW}⚠${NC} Frontend 容器未运行"
fi

# 4. API 健康检查
echo -e "\n🔗 4. API 健康检查"

if curl -s http://localhost:8000/health 2>/dev/null | grep -q "healthy"; then
    echo -e "   ${GREEN}✓${NC} Backend API (port 8000) 正常"
    ((PASS++))
else
    echo -e "   ${YELLOW}⚠${NC} Backend API 未响应"
fi

if curl -s http://localhost:8080/v1/meta 2>/dev/null | grep -q "version"; then
    echo -e "   ${GREEN}✓${NC} Weaviate (port 8080) 正常"
    ((PASS++))
else
    echo -e "   ${YELLOW}⚠${NC} Weaviate 未响应"
fi

if curl -s http://localhost:8501 2>/dev/null | grep -q "Streamlit"; then
    echo -e "   ${GREEN}✓${NC} Frontend (port 8501) 正常"
    ((PASS++))
else
    echo -e "   ${YELLOW}⚠${NC} Frontend 未响应"
fi

# 5. 总结
echo -e "\n========================================="
echo -e "检查结果: ${GREEN}通过 $PASS${NC} / 共 $((PASS+FAIL)) 项"
echo "========================================="

if [ $FAIL -eq 0 ] && [ $PASS -ge 6 ]; then
    echo -e "${GREEN}✅ Phase 0 基本完成！${NC}"
    echo ""
    echo "下一步："
    echo "1. 访问前端: http://localhost:8501"
    echo "2. 访问 API 文档: http://localhost:8000/docs"
    echo "3. 继续 Phase 1: Router"
else
    echo -e "${YELLOW}⚠️ Phase 0 未完全完成，请先启动服务：${NC}"
    echo "   docker-compose up -d --build"
fi
