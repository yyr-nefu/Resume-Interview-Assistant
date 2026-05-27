<template>
  <div class="notes-container">
    <div class="notes-header">
      <h2>学习笔记与收藏</h2>
      <p>管理你的学习内容</p>
    </div>
    
    <div class="notes-tabs">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="学习笔记" name="notes">
          <div class="notes-section">
            <div class="section-intro">
              <h3>个性化学习笔记</h3>
              <p>基于JD和能力缺口生成专属学习内容</p>
              <el-button type="primary" @click="generateNotes" :loading="generating">
                <Document />
                生成学习笔记
              </el-button>
            </div>
            
            <div class="notes-content" v-if="notesContent">
              <el-card>
                <div class="notes-text" v-html="formattedNotes"></div>
                <div class="notes-actions">
                  <el-button @click="copyNotes">
                    <DocumentCopy />
                    复制笔记
                  </el-button>
                  <el-button @click="saveNotes">
                    <FolderOpened />
                    保存到归档
                  </el-button>
                </div>
              </el-card>
            </div>
            
            <div class="empty-notes" v-else>
              <Memo :size="64" />
              <p>暂无学习笔记</p>
              <span>点击上方按钮生成基于JD的学习笔记</span>
            </div>
          </div>
        </el-tab-pane>
        
        <el-tab-pane label="收藏夹" name="favorites">
          <div class="favorites-section">
            <div class="favorites-header">
              <h3>收藏夹管理</h3>
              <el-button type="primary" @click="showCreateDialog">
                <Plus />
                新建收藏夹
              </el-button>
            </div>
            
            <div class="folders-grid">
              <div 
                v-for="folder in folders" 
                :key="folder.id"
                :class="['folder-card', { active: selectedFolder === folder.id }]"
                @click="selectFolder(folder.id)"
              >
                <div class="folder-icon">
                  <FolderOpened :size="32" />
                </div>
                <div class="folder-info">
                  <h4>{{ folder.name }}</h4>
                  <span>{{ folder.items.length }} 个收藏</span>
                </div>
                <el-dropdown trigger="click" @command="(cmd) => handleFolderCommand(cmd, folder)">
                  <el-button text size="small">
                    <MoreFilled />
                  </el-button>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item command="rename">重命名</el-dropdown-item>
                      <el-dropdown-item command="delete" divided>删除</el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </div>
              
              <div class="folder-card add-folder" @click="showCreateDialog">
                <div class="folder-icon">
                  <Plus :size="32" />
                </div>
                <div class="folder-info">
                  <h4>新建收藏夹</h4>
                  <span>添加新的收藏分类</span>
                </div>
              </div>
            </div>
            
            <div class="favorites-list" v-if="selectedFolder">
              <div class="list-header">
                <h3>{{ getCurrentFolderName() }}</h3>
                <el-button size="small" @click="clearFolderSelection">
                  取消选择
                </el-button>
              </div>
              
              <div class="favorite-items">
                <div 
                  v-for="item in getCurrentFolderItems()" 
                  :key="item.id"
                  class="favorite-item"
                >
                  <div class="item-content">
                    <div class="item-question" v-if="item.question">
                      <span class="label">问题：</span>
                      {{ item.question }}
                    </div>
                    <div class="item-answer">
                      <span class="label">回答：</span>
                      {{ item.answer }}
                    </div>
                    <div class="item-meta">
                      {{ formatDate(item.createdAt) }}
                    </div>
                  </div>
                  <div class="item-actions">
                    <el-button size="small" text @click="moveToFolder(item)">
                      <FolderOpened />
                      移动
                    </el-button>
                    <el-button size="small" text type="danger" @click="removeFromFavorites(item)">
                      <Delete />
                      删除
                    </el-button>
                  </div>
                </div>
                
                <div class="empty-items" v-if="getCurrentFolderItems().length === 0">
                  <p>该收藏夹暂无内容</p>
                </div>
              </div>
            </div>
            
            <div class="all-favorites" v-else>
              <div class="list-header">
                <h3>全部收藏</h3>
              </div>
              
              <div class="favorite-items">
                <div 
                  v-for="item in allFavorites" 
                  :key="item.id"
                  class="favorite-item"
                >
                  <div class="item-content">
                    <div class="item-question" v-if="item.question">
                      <span class="label">问题：</span>
                      {{ item.question }}
                    </div>
                    <div class="item-answer">
                      <span class="label">回答：</span>
                      {{ item.answer }}
                    </div>
                    <div class="item-meta">
                      {{ formatDate(item.createdAt) }}
                    </div>
                  </div>
                  <div class="item-actions">
                    <el-button size="small" text @click="moveToFolder(item)">
                      <FolderOpened />
                      移动
                    </el-button>
                    <el-button size="small" text type="danger" @click="removeFromFavorites(item)">
                      <Delete />
                      删除
                    </el-button>
                  </div>
                </div>
                
                <div class="empty-items" v-if="allFavorites.length === 0">
                  <Star :size="48" />
                  <p>暂无收藏</p>
                  <span>在面试过程中收藏你的满意回答</span>
                </div>
              </div>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
    
    <el-dialog
      v-model="createDialogVisible"
      title="新建收藏夹"
      width="400px"
    >
      <el-form :model="newFolder" label-position="top">
        <el-form-item label="收藏夹名称">
          <el-input v-model="newFolder.name" placeholder="请输入收藏夹名称" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="createDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="createFolder">创建</el-button>
      </template>
    </el-dialog>
    
    <el-dialog
      v-model="renameDialogVisible"
      title="重命名收藏夹"
      width="400px"
    >
      <el-form :model="renameForm" label-position="top">
        <el-form-item label="收藏夹名称">
          <el-input v-model="renameForm.name" placeholder="请输入新名称" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="renameDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmRename">确认</el-button>
      </template>
    </el-dialog>
    
    <el-dialog
      v-model="moveDialogVisible"
      title="移动到收藏夹"
      width="400px"
    >
      <el-form :model="moveForm" label-position="top">
        <el-form-item label="选择收藏夹">
          <el-select v-model="moveForm.folderId" placeholder="请选择收藏夹">
            <el-option 
              v-for="folder in folders" 
              :key="folder.id"
              :label="folder.name"
              :value="folder.id"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="moveDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmMove">移动</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { 
  Document, DocumentCopy, FolderOpened, Plus, MoreFilled, 
  Delete, Memo, Star 
} from '@element-plus/icons-vue'

const activeTab = ref('notes')
const notesContent = ref('')
const generating = ref(false)
const selectedFolder = ref(null)
const createDialogVisible = ref(false)
const renameDialogVisible = ref(false)
const moveDialogVisible = ref(false)

const newFolder = reactive({ name: '' })
const renameForm = reactive({ id: '', name: '' })
const moveForm = reactive({ item: null, folderId: '' })

const folders = ref([
  { id: 'default', name: '默认收藏夹', items: [] }
])

const allFavorites = computed(() => {
  return folders.value.reduce((acc, folder) => {
    return acc.concat(folder.items)
  }, [])
})

const formattedNotes = computed(() => {
  if (!notesContent.value) return ''
  return notesContent.value.replace(/\n/g, '<br>')
})

const showCreateDialog = () => {
  newFolder.name = ''
  createDialogVisible.value = true
}

const createFolder = () => {
  if (!newFolder.name.trim()) {
    ElMessage.warning('请输入收藏夹名称')
    return
  }
  
  folders.value.push({
    id: `folder_${Date.now()}`,
    name: newFolder.name,
    items: []
  })
  
  saveFolders()
  createDialogVisible.value = false
  ElMessage.success('收藏夹创建成功')
}

const selectFolder = (folderId) => {
  selectedFolder.value = selectedFolder.value === folderId ? null : folderId
}

const clearFolderSelection = () => {
  selectedFolder.value = null
}

const getCurrentFolderName = () => {
  const folder = folders.value.find(f => f.id === selectedFolder.value)
  return folder ? folder.name : ''
}

const getCurrentFolderItems = () => {
  const folder = folders.value.find(f => f.id === selectedFolder.value)
  return folder ? folder.items : []
}

const handleFolderCommand = (command, folder) => {
  if (command === 'rename') {
    renameForm.id = folder.id
    renameForm.name = folder.name
    renameDialogVisible.value = true
  } else if (command === 'delete') {
    deleteFolder(folder.id)
  }
}

const confirmRename = () => {
  if (!renameForm.name.trim()) {
    ElMessage.warning('请输入收藏夹名称')
    return
  }
  
  const folder = folders.value.find(f => f.id === renameForm.id)
  if (folder) {
    folder.name = renameForm.name
    saveFolders()
    ElMessage.success('收藏夹重命名成功')
  }
  
  renameDialogVisible.value = false
}

const deleteFolder = (folderId) => {
  if (folderId === 'default') {
    ElMessage.warning('默认收藏夹不能删除')
    return
  }
  
  const folder = folders.value.find(f => f.id === folderId)
  if (folder && folder.items.length > 0) {
    // 将项目移动到默认收藏夹
    const defaultFolder = folders.value.find(f => f.id === 'default')
    defaultFolder.items.push(...folder.items)
  }
  
  folders.value = folders.value.filter(f => f.id !== folderId)
  if (selectedFolder.value === folderId) {
    selectedFolder.value = null
  }
  
  saveFolders()
  ElMessage.success('收藏夹已删除')
}

const moveToFolder = (item) => {
  moveForm.item = item
  moveForm.folderId = ''
  moveDialogVisible.value = true
}

const confirmMove = () => {
  if (!moveForm.folderId) {
    ElMessage.warning('请选择收藏夹')
    return
  }
  
  // 从原位置移除
  folders.value.forEach(folder => {
    folder.items = folder.items.filter(i => i.id !== moveForm.item.id)
  })
  
  // 添加到新位置
  const targetFolder = folders.value.find(f => f.id === moveForm.folderId)
  if (targetFolder) {
    targetFolder.items.push(moveForm.item)
  }
  
  saveFolders()
  moveDialogVisible.value = false
  ElMessage.success('已移动到收藏夹')
}

const removeFromFavorites = (item) => {
  folders.value.forEach(folder => {
    folder.items = folder.items.filter(i => i.id !== item.id)
  })
  saveFolders()
  ElMessage.success('已从收藏夹移除')
}

const generateNotes = () => {
  generating.value = true
  
  setTimeout(() => {
    const jdContent = localStorage.getItem('jdContent') || ''
    
    notesContent.value = `基于您提供的JD，我们为您生成以下学习笔记：

一、岗位技能分析

根据JD要求，该岗位需要掌握以下核心技能：
1. 基础知识：数据结构、算法、网络原理
2. 专业技能：相关技术栈的使用
3. 软技能：沟通能力、团队协作

二、学习计划建议

第一周：基础知识复习
- 回顾核心数据结构
- 练习基础算法题

第二周：专业技能学习
- 学习岗位要求的技术栈
- 完成小型项目实战

第三周：综合提升
- 模拟面试练习
- 项目经验整理

三、面试准备要点

1. 准备好自我介绍，突出与岗位相关的经验
2. 复习项目中用到的技术细节
3. 准备几个能体现问题解决能力的案例

四、资源推荐

推荐学习资源：
- 官方文档
- 技术博客
- 在线课程

祝您面试成功！`
    
    generating.value = false
    ElMessage.success('学习笔记生成成功')
  }, 2000)
}

const copyNotes = () => {
  navigator.clipboard.writeText(notesContent.value)
  ElMessage.success('笔记已复制到剪贴板')
}

const saveNotes = () => {
  const archives = JSON.parse(localStorage.getItem('archives') || '[]')
  archives.push({
    id: `note_${Date.now()}`,
    type: 'note',
    name: `学习笔记_${new Date().toLocaleDateString()}`,
    content: notesContent.value,
    createdAt: new Date().toISOString()
  })
  localStorage.setItem('archives', JSON.stringify(archives))
  ElMessage.success('笔记已保存到归档')
}

const formatDate = (dateStr) => {
  return new Date(dateStr).toLocaleDateString('zh-CN')
}

const saveFolders = () => {
  localStorage.setItem('favoriteFolders', JSON.stringify(folders.value))
}

const loadFolders = () => {
  const saved = localStorage.getItem('favoriteFolders')
  if (saved) {
    folders.value = JSON.parse(saved)
  }
  
  // 合并独立收藏
  const savedFavorites = JSON.parse(localStorage.getItem('favorites') || '[]')
  if (savedFavorites.length > 0) {
    const defaultFolder = folders.value.find(f => f.id === 'default')
    if (defaultFolder) {
      defaultFolder.items = [...defaultFolder.items, ...savedFavorites]
      localStorage.removeItem('favorites')
    }
    saveFolders()
  }
}

onMounted(() => {
  loadFolders()
})
</script>

<style scoped>
.notes-container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 24px;
}

.notes-header {
  text-align: center;
  margin-bottom: 40px;
}

.notes-header h2 {
  font-size: 32px;
  font-weight: 700;
  color: #1d1d1f;
  margin-bottom: 10px;
  letter-spacing: -0.3px;
}

.notes-header p {
  color: #6b7280;
  font-size: 15px;
}

.notes-tabs :deep(.el-tabs__header) {
  margin-bottom: 28px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e5e7eb;
}

.notes-tabs :deep(.el-tabs__item) {
  font-size: 16px;
  font-weight: 500;
  color: #6b7280;
  padding: 0 20px;
  margin-right: 24px;
}

.notes-tabs :deep(.el-tabs__item.is-active) {
  color: #007aff;
  font-weight: 600;
}

.notes-tabs :deep(.el-tabs__active-bar) {
  background: linear-gradient(90deg, #007aff 0%, #5856d6 100%);
  height: 3px;
  border-radius: 2px;
}

.section-intro {
  text-align: center;
  padding: 56px 40px;
  background: linear-gradient(135deg, #f8f9fa 0%, #f3f4f6 100%);
  border-radius: 20px;
  margin-bottom: 28px;
  border: 1px solid #e5e7eb;
}

.section-intro h3 {
  font-size: 22px;
  color: #1d1d1f;
  margin-bottom: 10px;
  font-weight: 600;
}

.section-intro p {
  color: #6b7280;
  margin-bottom: 24px;
  font-size: 15px;
}

.section-intro :deep(.el-button--primary) {
  padding: 14px 32px;
  border-radius: 14px;
  font-size: 15px;
  font-weight: 600;
  background: linear-gradient(135deg, #007aff 0%, #5856d6 100%);
  border: none;
  box-shadow: 0 4px 16px rgba(0, 122, 255, 0.3);
}

.notes-content :deep(.el-card) {
  border-radius: 16px;
  border: 1px solid #e5e7eb;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
}

.notes-content :deep(.el-card__body) {
  padding: 32px;
}

.notes-text {
  line-height: 1.8;
  color: #374151;
  white-space: pre-wrap;
  margin-bottom: 24px;
  font-size: 15px;
}

.notes-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
  padding-top: 24px;
  border-top: 1px solid #e5e7eb;
}

.notes-actions :deep(.el-button) {
  padding: 10px 24px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 500;
}

.empty-notes {
  text-align: center;
  padding: 80px 20px;
  color: #6b7280;
}

.empty-notes :deep(.el-icon) {
  color: #9ca3af;
  margin-bottom: 20px;
}

.empty-notes p {
  font-size: 16px;
  margin: 0 0 8px 0;
  color: #374151;
}

.empty-notes span {
  font-size: 14px;
  color: #9ca3af;
}

.favorites-section {
  padding: 0;
}

.favorites-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.favorites-header h3 {
  font-size: 20px;
  color: #1d1d1f;
  margin: 0;
  font-weight: 600;
}

.favorites-header :deep(.el-button--primary) {
  padding: 10px 20px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 500;
  background: linear-gradient(135deg, #007aff 0%, #5856d6 100%);
  border: none;
}

.folders-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
  margin-bottom: 36px;
}

.folder-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 20px;
  background: #ffffff;
  border: 2px solid #f3f4f6;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.folder-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #007aff 0%, #5856d6 100%);
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.folder-card:hover {
  border-color: #007aff;
  box-shadow: 0 4px 20px rgba(0, 122, 255, 0.1);
  transform: translateY(-2px);
}

.folder-card:hover::before {
  transform: scaleX(1);
}

.folder-card.active {
  border-color: #007aff;
  background: #f0f7ff;
}

.folder-card.active::before {
  transform: scaleX(1);
}

.folder-card.add-folder {
  border-style: dashed;
  border-color: #d1d5db;
  color: #9ca3af;
}

.folder-card.add-folder:hover {
  border-color: #007aff;
  color: #007aff;
  background: #f0f7ff;
}

.folder-icon {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(0, 122, 255, 0.1) 0%, rgba(88, 86, 214, 0.1) 100%);
  border-radius: 12px;
  color: #007aff;
}

.folder-card.add-folder .folder-icon {
  background: transparent;
}

.folder-info {
  flex: 1;
  min-width: 0;
}

.folder-info h4 {
  font-size: 15px;
  color: #1d1d1f;
  margin: 0 0 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-weight: 600;
}

.folder-info span {
  font-size: 13px;
  color: #6b7280;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e5e7eb;
}

.list-header h3 {
  font-size: 18px;
  color: #1d1d1f;
  margin: 0;
  font-weight: 600;
}

.list-header :deep(.el-button) {
  font-size: 13px;
  color: #6b7280;
  padding: 6px 14px;
}

.favorite-items {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.favorite-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 20px;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  gap: 20px;
  transition: all 0.25s ease;
}

.favorite-item:hover {
  border-color: #007aff;
  box-shadow: 0 2px 12px rgba(0, 122, 255, 0.08);
}

.item-content {
  flex: 1;
  min-width: 0;
}

.item-question {
  color: #1d1d1f;
  margin-bottom: 10px;
  line-height: 1.6;
  font-size: 15px;
  font-weight: 500;
}

.item-question .label {
  color: #007aff;
  font-weight: 600;
}

.item-answer {
  color: #374151;
  line-height: 1.6;
  font-size: 14px;
}

.item-answer .label {
  color: #22c55e;
  font-weight: 600;
}

.item-meta {
  margin-top: 10px;
  font-size: 12px;
  color: #9ca3af;
}

.item-actions {
  display: flex;
  gap: 10px;
  flex-shrink: 0;
}

.item-actions :deep(.el-button) {
  padding: 6px 14px;
  font-size: 12px;
  border-radius: 8px;
}

.item-actions :deep(.el-button--text) {
  color: #6b7280;
}

.item-actions :deep(.el-button--text:hover) {
  color: #007aff;
  background: rgba(0, 122, 255, 0.05);
}

.empty-items {
  text-align: center;
  padding: 60px 20px;
  color: #6b7280;
}

.empty-items :deep(.el-icon) {
  color: #9ca3af;
  margin-bottom: 16px;
}

.empty-items p {
  margin: 0 0 6px 0;
  font-size: 15px;
  color: #374151;
}

.empty-items span {
  font-size: 13px;
  color: #9ca3af;
}

@media (max-width: 768px) {
  .notes-container {
    padding: 16px;
  }
  
  .notes-header h2 {
    font-size: 26px;
  }
  
  .section-intro {
    padding: 40px 24px;
  }
  
  .section-intro h3 {
    font-size: 18px;
  }
  
  .folders-grid {
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 14px;
  }
  
  .folder-card {
    padding: 16px;
  }
  
  .folder-icon {
    width: 36px;
    height: 36px;
  }
  
  .favorite-item {
    padding: 16px;
    flex-direction: column;
    gap: 14px;
  }
  
  .item-actions {
    justify-content: flex-end;
  }
}
</style>
