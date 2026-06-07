<template>
  <div class="resume-optimize-container">
    <div class="section-header">
      <h2>简历重构润色</h2>
      <p>基于目标岗位属性，优化简历表达和结构</p>
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
          <el-form-item label="原始简历">
            <el-textarea 
              v-model="form.resumeContent" 
              :rows="8" 
              placeholder="请粘贴原始简历内容"
              class="resume-textarea"
            />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" size="large" @click="optimizeResume" :loading="loading">
              <MagicStick />
              开始优化
            </el-button>
          </el-form-item>
        </el-form>
      </div>
      
      <div class="result-section" v-if="result">
        <el-card title="优化结果">
          <div class="word-count">
            <span class="label">字数统计：</span>
            <span class="value">{{ result.word_count }} 字</span>
            <el-tag :type="result.word_count > 2000 ? 'warning' : 'success'">
              {{ result.word_count > 2000 ? '建议精简至2页内' : '篇幅合适' }}
            </el-tag>
          </div>
          
          <div class="optimized-content">
            <h4>优化后的简历</h4>
            <el-textarea 
              :value="result.optimized_resume" 
              :rows="15" 
              readonly
              class="optimized-textarea"
            />
          </div>
          
          <div class="suggestions">
            <h4>优化建议</h4>
            <ul>
              <li v-for="(suggestion, index) in result.suggestions" :key="index">
                <Sunny />
                {{ suggestion }}
              </li>
            </ul>
          </div>
          
          <div class="action-buttons">
            <el-button type="primary" @click="copyResume">
              <DocumentCopy />
              复制简历
            </el-button>
            <el-button @click="downloadResume">
              <Download />
              下载简历
            </el-button>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAppStore } from '@/stores/app'
import { resumeApi } from '@/utils/api'
import { MagicStick, Sunny, DocumentCopy, Download } from '@element-plus/icons-vue'

const router = useRouter()
const appStore = useAppStore()

const form = reactive({
  positionType: 'dev',
  resumeContent: ''
})

const loading = ref(false)
const result = ref(null)
const currentJdId = ref('')

onMounted(() => {
  const savedResume = localStorage.getItem('currentResume')
  if (savedResume) {
    form.resumeContent = savedResume
  }

  // 尝试从store或localStorage获取JD ID
  const jdData = localStorage.getItem('currentJD')
  if (jdData) {
    try {
      const parsed = JSON.parse(jdData)
      // 如果有保存的JD ID就使用，否则使用默认值
      currentJdId.value = parsed.jd_id || 'jd_1'
    } catch (e) {
      currentJdId.value = 'jd_1'
    }
  } else {
    currentJdId.value = 'jd_1'
  }

  // 从store获取岗位类型（如果用户在JD解析页面选择过）
  if (appStore.positionType) {
    form.positionType = appStore.positionType
  }
})

const optimizeResume = async () => {
  if (!form.resumeContent.trim()) {
    alert('请输入简历内容')
    return
  }

  loading.value = true
  try {
    const response = await resumeApi.optimize(
      form.resumeContent,
      currentJdId.value,
      form.positionType
    )
    result.value = response
  } catch (error) {
    console.error('优化失败:', error)
    alert('优化失败，请重试。请确保已先进行JD解析。')
  } finally {
    loading.value = false
  }
}

const copyResume = () => {
  navigator.clipboard.writeText(result.value.optimized_resume)
  alert('已复制到剪贴板')
}

const downloadResume = () => {
  const blob = new Blob([result.value.optimized_resume], { type: 'text/plain;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = '优化后的简历.txt'
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}
</script>

<style scoped>
.resume-optimize-container {
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

.input-section :deep(.el-button--primary) {
  background: #007aff;
  border: none;
  color: #ffffff;
  font-weight: 500;
  border-radius: 8px;
}

.resume-textarea {
  width: 100%;
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

.word-count {
  margin-bottom: 16px;
  padding: 14px;
  background: #f5f5f7;
  border-radius: 8px;
}

.word-count .label {
  font-weight: 500;
  color: #86868b;
}

.word-count .value {
  font-size: 18px;
  color: #007aff;
  font-weight: 600;
}

.optimized-content {
  margin-bottom: 16px;
}

.optimized-content h4 {
  margin-bottom: 10px;
  color: #1d1d1f;
  font-size: 15px;
}

.optimized-textarea {
  width: 100%;
  background: #fafafa;
  border: 1px solid #e8e8e8;
  border-radius: 8px;
}

.suggestions {
  margin-bottom: 16px;
  padding: 16px;
  background: #fff9f0;
  border: 1px solid #ffedd5;
  border-radius: 12px;
}

.suggestions h4 {
  margin-bottom: 10px;
  color: #1d1d1f;
  font-size: 14px;
}

.suggestions ul {
  padding-left: 20px;
}

.suggestions li {
  margin-bottom: 8px;
  color: #333333;
  font-size: 13px;
}

.action-buttons {
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