<template>
  <div class="jd-parse-container">
    <div class="section-header">
      <h2>JD智能解析</h2>
      <p>上传或粘贴岗位JD，智能拆解岗位要求</p>
    </div>
    
    <div class="main-content">
      <div class="input-section">
        <el-form :model="form" label-width="80px">
          <el-form-item label="岗位类型">
            <el-select v-model="form.positionType" placeholder="请选择岗位类型">
              <el-option label="开发岗" value="dev" />
              <el-option label="产品岗" value="product" />
              <el-option label="数据岗" value="data" />
              <el-option label="实施岗" value="implementation" />
            </el-select>
          </el-form-item>
          <el-form-item label="JD内容">
            <el-textarea 
              v-model="form.jdContent" 
              :rows="10" 
              placeholder="请粘贴JD内容或上传JD文件"
              class="jd-textarea"
            />
          </el-form-item>
          <el-form-item>
            <el-upload
              class="jd-upload"
              :auto-upload="false"
              :show-file-list="false"
              accept=".txt,.docx,.pdf"
              @change="handleFileChange"
            >
              <el-button size="small" type="primary">
                <Upload />
                上传JD文件
              </el-button>
            </el-upload>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" size="large" @click="parseJD" :loading="loading">
              <Search />
              开始解析
            </el-button>
          </el-form-item>
        </el-form>
      </div>
      
      <div class="result-section" v-if="result">
        <el-card title="解析结果">
          <el-tabs v-model="activeTab">
            <el-tab-pane label="技术能力" name="technical">
              <el-tag v-for="skill in result.technical_skills" :key="skill" class="skill-tag">
                {{ skill }}
              </el-tag>
            </el-tab-pane>
            <el-tab-pane label="软素质" name="soft">
              <el-tag v-for="skill in result.soft_skills" :key="skill" class="skill-tag">
                {{ skill }}
              </el-tag>
            </el-tab-pane>
            <el-tab-pane label="岗位常识" name="knowledge">
              <el-tag v-for="item in result.position_knowledge" :key="item" class="skill-tag">
                {{ item }}
              </el-tag>
            </el-tab-pane>
            <el-tab-pane label="基础要求" name="basic">
              <ul class="requirement-list">
                <li v-for="(item, index) in result.basic_requirements" :key="index">
                  {{ item }}
                </li>
              </ul>
            </el-tab-pane>
            <el-tab-pane label="加分项" name="bonus">
              <ul class="requirement-list">
                <li v-for="(item, index) in result.bonus_points" :key="index">
                  {{ item }}
                </li>
              </ul>
            </el-tab-pane>
          </el-tabs>
          
          <div class="action-buttons">
            <el-button type="primary" @click="goToResumeAnalysis">
              <User />
              进行简历诊断
            </el-button>
            <el-button @click="copyResult">
              <DocumentCopy />
              复制结果
            </el-button>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAppStore } from '@/stores/app'
import axios from 'axios'
import { Upload, Search, User, DocumentCopy } from '@element-plus/icons-vue'

const router = useRouter()
const appStore = useAppStore()

const form = reactive({
  positionType: 'dev',
  jdContent: ''
})

const loading = ref(false)
const result = ref(null)
const activeTab = ref('technical')

const handleFileChange = (file) => {
  const reader = new FileReader()
  reader.onload = (e) => {
    form.jdContent = e.target.result.slice(0, 10000)
  }
  reader.readAsText(file.raw)
}

const parseJD = async () => {
  if (!form.jdContent.trim()) {
    alert('请输入JD内容')
    return
  }

  loading.value = true
  try {
    const response = await axios.post('/api/jd/parse', {
      jd_content: form.jdContent,
      position_type: form.positionType
    })
    result.value = response.data

    // 保存到localStorage和store
    localStorage.setItem('currentJD', JSON.stringify({
      ...response.data,
      jd_id: `jd_${Date.now()}`,
      position_type: form.positionType,
      content: form.jdContent
    }))

    // 更新store
    appStore.setPositionType(form.positionType)
    appStore.setCurrentJdId(`jd_${Date.now()}`)
  } catch (error) {
    console.error('解析失败:', error)
    alert('解析失败，请重试')
  } finally {
    loading.value = false
  }
}

const goToResumeAnalysis = () => {
  router.push('/resume-analysis')
}

const copyResult = () => {
  const text = JSON.stringify(result.value, null, 2)
  navigator.clipboard.writeText(text)
  alert('已复制到剪贴板')
}
</script>

<style scoped>
.jd-parse-container {
  max-width: 900px;
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

.main-content {
  display: grid;
  gap: 20px;
}

.input-section {
  background: #ffffff;
  border: 1px solid #e8e8e8;
  border-radius: 16px;
  padding: 28px;
}

.input-section :deep(.el-form-item__label) {
  color: #333333;
  font-weight: 500;
}

.input-section :deep(.el-select),
.input-section :deep(.el-textarea) {
  background: #ffffff;
  border: 1px solid #d1d1d6;
  color: #1d1d1f;
  border-radius: 8px;
}

.input-section :deep(.el-select:hover),
.input-section :deep(.el-textarea:hover) {
  border-color: #007aff;
}

.input-section :deep(.el-button--primary) {
  background: #007aff;
  border: none;
  color: #ffffff;
  font-weight: 500;
  border-radius: 8px;
}

.jd-textarea {
  width: 100%;
}

.jd-upload {
  margin-bottom: 16px;
}

.result-section {
  animation: fadeIn 0.3s ease;
}

.result-section :deep(.el-card) {
  background: #ffffff;
  border: 1px solid #e8e8e8;
  border-radius: 16px;
}

.result-section :deep(.el-card__header) {
  border-bottom: 1px solid #e8e8e8;
  color: #1d1d1f;
  font-weight: 600;
}

.result-section :deep(.el-tabs__item) {
  color: #86868b;
}

.result-section :deep(.el-tabs__item.is-active) {
  color: #007aff;
}

.result-section :deep(.el-tabs__active-bar) {
  background: #007aff;
}

.skill-tag {
  margin: 6px;
  background: #f0f7ff;
  border: 1px solid #cce5ff;
  color: #007aff;
}

.requirement-list {
  padding-left: 0;
  list-style: none;
}

.requirement-list li {
  margin-bottom: 10px;
  padding: 12px 14px;
  background: #f5f5f7;
  border-radius: 8px;
  color: #333333;
  font-size: 14px;
}

.action-buttons {
  margin-top: 20px;
  display: flex;
  gap: 10px;
}

.action-buttons :deep(.el-button--primary) {
  background: #007aff;
  border: none;
  color: #ffffff;
  font-weight: 500;
  border-radius: 8px;
}

.action-buttons :deep(.el-button--default) {
  background: transparent;
  border: 1px solid #d1d1d6;
  color: #333333;
  border-radius: 8px;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>