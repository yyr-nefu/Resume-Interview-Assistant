<template>
  <div class="archive-container">
    <div class="section-header">
      <h2>岗位文件归档</h2>
      <p>按岗位维度分类归档，支持多版本对比</p>
    </div>
    
    <div class="main-content">
      <div class="filter-section">
        <el-select v-model="filterJdId" placeholder="按JD筛选">
          <el-option label="全部" value="" />
          <el-option label="JD 1" value="jd_1" />
        </el-select>
        <el-select v-model="filterType" placeholder="按类型筛选">
          <el-option label="全部" value="" />
          <el-option label="JD解析" value="jd" />
          <el-option label="面试记录" value="interview" />
          <el-option label="学习笔记" value="note" />
          <el-option label="简历" value="resume" />
        </el-select>
        <el-button type="primary" size="small" @click="refreshList">
          <Refresh />
          刷新
        </el-button>
      </div>
      
      <div class="archive-list">
        <div class="archive-card" v-for="item in filteredItems" :key="item.id">
          <div class="card-header">
            <div class="item-icon">
              <component :is="getItemIcon(item.type)" :size="32" />
            </div>
            <div class="item-info">
              <div class="item-name">{{ item.name }}</div>
              <div class="item-meta">
                <span class="item-type">{{ getItemTypeName(item.type) }}</span>
                <span class="item-date">{{ formatDate(item.created_at) }}</span>
              </div>
            </div>
          </div>
          <div class="card-actions">
            <el-button size="small" @click="viewItem(item)">
              <View />
              查看
            </el-button>
            <el-button size="small" @click="compareItem(item)">
              <Connection />
              对比
            </el-button>
            <el-button size="small" type="danger" @click="deleteItem(item)">
              <Delete />
              删除
            </el-button>
          </div>
        </div>
        
        <div class="empty-state" v-if="filteredItems.length === 0">
          <FolderOpened :size="64" />
          <p>暂无归档文件</p>
        </div>
      </div>
      
      <div class="compare-modal" v-if="compareItems.length > 0">
        <el-card title="文件对比">
          <div class="compare-content">
            <div class="compare-item" v-for="(item, index) in compareItems" :key="index">
              <div class="compare-header">{{ item.name }}</div>
              <pre class="compare-body">{{ item.data?.content || '暂无内容' }}</pre>
            </div>
          </div>
          <div class="compare-actions">
            <el-button @click="clearCompare">关闭对比</el-button>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, markRaw } from 'vue'
import axios from 'axios'
import { Refresh, Document, ChatDotRound, Memo, User, View, Connection, Delete, FolderOpened } from '@element-plus/icons-vue'

const items = ref([])
const filterJdId = ref('')
const filterType = ref('')
const compareItems = ref([])

const filteredItems = computed(() => {
  return items.value.filter(item => {
    if (filterJdId.value && item.jd_id !== filterJdId.value) return false
    if (filterType.value && item.type !== filterType.value) return false
    return true
  })
})

const getItemIcon = (type) => {
  const icons = {
    'jd': markRaw(Document),
    'interview': markRaw(ChatDotRound),
    'note': markRaw(Memo),
    'resume': markRaw(User),
    'unknown': markRaw(Document)
  }
  return icons[type] || markRaw(Document)
}

const getItemTypeName = (type) => {
  const names = {
    'jd': 'JD解析',
    'interview': '面试记录',
    'note': '学习笔记',
    'resume': '简历',
    'unknown': '未知'
  }
  return names[type] || '未知'
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleString('zh-CN')
}

const loadItems = async () => {
  try {
    const response = await axios.get('/api/archive/list')
    items.value = response.data.items
  } catch (error) {
    console.error('加载归档失败:', error)
  }
}

const refreshList = () => {
  loadItems()
}

const viewItem = async (item) => {
  try {
    const response = await axios.get(`/api/archive/get/${item.id}`)
    const content = response.data.content || JSON.stringify(response.data, null, 2)
    alert(content.slice(0, 2000))
  } catch (error) {
    console.error('查看文件失败:', error)
    alert('查看失败')
  }
}

const compareItem = async (item) => {
  if (compareItems.value.length >= 2) {
    compareItems.value = []
  }
  
  try {
    const response = await axios.get(`/api/archive/get/${item.id}`)
    compareItems.value.push({ ...item, data: response.data })
  } catch (error) {
    console.error('获取文件失败:', error)
  }
}

const clearCompare = () => {
  compareItems.value = []
}

const deleteItem = async (item) => {
  if (!confirm('确定要删除这个文件吗？')) return
  
  try {
    await axios.delete(`/api/archive/delete/${item.id}`)
    loadItems()
    alert('删除成功')
  } catch (error) {
    console.error('删除失败:', error)
    alert('删除失败')
  }
}

onMounted(() => {
  loadItems()
})
</script>

<style scoped>
.archive-container {
  max-width: 850px;
  margin: 0 auto;
}

.section-header {
  text-align: center;
  margin-bottom: 40px;
}

.section-header h2 {
  font-size: clamp(1.5rem, 3vw, 2rem);
  font-weight: 600;
  color: #1d1d1f;
  margin-bottom: 8px;
}

.section-header p {
  color: #86868b;
  font-size: 14px;
}

.filter-section {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  padding: 16px;
  background: #ffffff;
  border: 1px solid #e8e8e8;
  border-radius: 12px;
}

.filter-section :deep(.el-select) {
  background: #ffffff;
  border: 1px solid #d1d1d6;
  color: #1d1d1f;
  border-radius: 8px;
}

.filter-section :deep(.el-button--primary) {
  background: #007aff;
  border: none;
  color: #ffffff;
  font-weight: 500;
  border-radius: 8px;
}

.archive-list {
  display: grid;
  gap: 12px;
}

.archive-card {
  background: #ffffff;
  border: 1px solid #e8e8e8;
  border-radius: 12px;
  padding: 18px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.2s ease;
}

.archive-card:hover {
  border-color: #007aff;
  background: #fafafa;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 14px;
}

.item-icon {
  width: 46px;
  height: 46px;
  background: linear-gradient(135deg, #007aff 0%, #5856d6 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.item-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.item-name {
  font-weight: 600;
  color: #1d1d1f;
  font-size: 15px;
}

.item-meta {
  display: flex;
  gap: 10px;
  color: #86868b;
  font-size: 13px;
}

.item-type {
  padding: 2px 8px;
  background: #f0f7ff;
  border: 1px solid #cce5ff;
  border-radius: 4px;
  color: #007aff;
}

.card-actions {
  display: flex;
  gap: 8px;
}

.card-actions :deep(.el-button) {
  padding: 6px 14px;
  border-radius: 6px;
  font-size: 13px;
}

.card-actions :deep(.el-button--text) {
  color: #86868b;
}

.card-actions :deep(.el-button--text:hover) {
  color: #007aff;
}

.empty-state {
  text-align: center;
  padding: 60px;
  color: #86868b;
}

.empty-state p {
  margin-top: 10px;
  font-size: 14px;
}

.compare-modal {
  margin-top: 24px;
  animation: fadeIn 0.3s ease;
}

.compare-content {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.compare-header {
  font-weight: bold;
  margin-bottom: 10px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.compare-body {
  background: #f5f5f5;
  padding: 15px;
  border-radius: 8px;
  max-height: 300px;
  overflow-y: auto;
  font-size: 14px;
}

.compare-actions {
  margin-top: 20px;
  text-align: right;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>