<template>
  <div class="resume-analysis-container">
    <div class="section-header">
      <h2>简历能力缺口诊断</h2>
      <p>粘贴JD和简历内容，智能分析能力匹配度</p>
    </div>
    
    <div class="main-content">
      <div class="input-section">
        <el-form :model="form" label-width="80px">
          <el-form-item label="JD内容">
            <el-textarea 
              v-model="form.jdContent" 
              :rows="8" 
              placeholder="请粘贴岗位JD内容..."
              class="jd-textarea"
            />
          </el-form-item>
          <el-form-item label="简历内容">
            <el-textarea 
              v-model="form.resumeContent" 
              :rows="10" 
              placeholder="请粘贴简历内容..."
              class="resume-textarea"
            />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" size="large" @click="analyzeResume" :loading="loading">
              <Finished />
              开始诊断
            </el-button>
          </el-form-item>
        </el-form>
      </div>
      
      <div class="result-section" v-if="result">
        <el-card title="诊断结果">
          <div class="score-display">
            <div class="score-circle">
              <span class="score-value">{{ result.score }}</span>
              <span class="score-unit">分</span>
            </div>
            <div class="score-label">匹配度</div>
          </div>
          
          <el-row :gutter="20">
            <el-col :span="8">
              <div class="result-box matched">
                <h4>已匹配能力</h4>
                <el-tag v-for="skill in result.matched_skills" :key="skill" class="skill-tag">
                  {{ skill }}
                </el-tag>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="result-box gap">
                <h4>能力缺口</h4>
                <el-tag v-for="skill in result.gap_skills" :key="skill" class="skill-tag">
                  {{ skill }}
                </el-tag>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="result-box bonus">
                <h4>可提升加分项</h4>
                <el-tag v-for="item in result.bonus_opportunities" :key="item" class="skill-tag">
                  {{ item }}
                </el-tag>
              </div>
            </el-col>
          </el-row>
          
          <div class="action-buttons">
            <el-button type="primary" @click="goToOptimize">
              <MagicStick />
              简历优化
            </el-button>
            <el-button @click="goToNotes">
              <Memo />
              生成学习笔记
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
import axios from 'axios'
import { Finished, MagicStick, Memo } from '@element-plus/icons-vue'

const router = useRouter()

const form = reactive({
  jdContent: '',
  resumeContent: ''
})

const loading = ref(false)
const result = ref(null)

const analyzeResume = async () => {
  if (!form.jdContent.trim()) {
    alert('请输入JD内容')
    return
  }
  
  if (!form.resumeContent.trim()) {
    alert('请输入简历内容')
    return
  }
  
  loading.value = true
  try {
    const response = await axios.post('/api/resume/analyze', {
      resume_content: form.resumeContent,
      jd_content: form.jdContent
    })
    result.value = response.data
    localStorage.setItem('resumeAnalysis', JSON.stringify(response.data))
    localStorage.setItem('currentResume', form.resumeContent)
    localStorage.setItem('currentJD', form.jdContent)
  } catch (error) {
    console.error('诊断失败:', error)
    alert('诊断失败，请重试')
  } finally {
    loading.value = false
  }
}

const goToOptimize = () => {
  router.push('/resume-optimize')
}

const goToNotes = () => {
  router.push('/notes')
}
</script>

<style scoped>
.resume-analysis-container {
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

.jd-textarea,
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

.score-display {
  text-align: center;
  margin-bottom: 30px;
}

.score-circle {
  width: 110px;
  height: 110px;
  border-radius: 50%;
  background: linear-gradient(135deg, #007aff 0%, #5856d6 100%);
  display: flex;
  align-items: baseline;
  justify-content: center;
  margin: 0 auto;
  padding-top: 28px;
}

.score-value {
  font-size: 44px;
  font-weight: 600;
  color: white;
}

.score-unit {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.8);
}

.score-label {
  margin-top: 10px;
  color: #86868b;
  font-size: 14px;
}

.result-box {
  padding: 18px;
  border-radius: 12px;
}

.result-box.matched {
  background: #f0f7ff;
  border: 1px solid #e0efff;
}

.result-box.gap {
  background: #fff9f0;
  border: 1px solid #ffedd5;
}

.result-box.bonus {
  background: #f0fff4;
  border: 1px solid #e6ffed;
}

.result-box h4 {
  margin-bottom: 12px;
  font-size: 15px;
  color: #1d1d1f;
}

.skill-tag {
  margin: 5px;
  background: rgba(0, 122, 255, 0.1);
  border: 1px solid rgba(0, 122, 255, 0.2);
  color: #007aff;
}

.action-buttons {
  margin-top: 24px;
  display: flex;
  gap: 10px;
  justify-content: center;
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
