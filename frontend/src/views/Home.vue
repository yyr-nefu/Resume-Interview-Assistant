<template>
  <div class="home-container">
    <div class="hero-section">
      <div class="hero-content">
        <div class="hero-icon">
          <Star />
        </div>
        <h1 class="hero-title">AI智能求职助手</h1>
        <p class="hero-subtitle">让AI帮你提升求职竞争力，轻松拿到心仪offer</p>
      </div>
    </div>
    
    <div class="main-card">
      <div class="card-header">
        <div class="header-icon">
          <Aim />
        </div>
        <div class="header-text">
          <h2>岗位匹配分析</h2>
          <p>粘贴JD和上传简历，获取专业的能力评估</p>
        </div>
      </div>
      
      <el-form :model="form" label-position="top">
        <el-form-item label="岗位JD内容">
          <div class="textarea-wrapper">
            <el-input
              type="textarea"
              v-model="form.jdContent"
              :rows="7"
              placeholder="请粘贴岗位JD内容..."
              class="jd-textarea"
            />
            <div class="textarea-hint">
              <CopyDocument />
              <span>粘贴完整的岗位描述以获得更准确的分析结果</span>
            </div>
          </div>
        </el-form-item>
        
        <el-form-item label="简历文件">
          <div class="upload-wrapper">
            <el-upload
              class="resume-upload"
              drag
              :auto-upload="false"
              :show-file-list="false"
              accept=".pdf,.doc,.docx,.txt"
              @change="handleResumeUpload"
            >
              <div class="upload-content">
                <div class="upload-icon">
                  <Upload />
                </div>
                <div class="upload-text">
                  <span>{{ resumeFileName ? '重新上传简历' : '将简历文件拖到此处，或点击上传' }}</span>
                  <span class="upload-format">支持 PDF、Word、TXT 格式</span>
                </div>
              </div>
            </el-upload>
            
            <div v-if="resumeFileName" class="uploaded-file">
              <div class="file-info">
                <Document />
                <span>{{ resumeFileName }}</span>
              </div>
              <el-button type="danger" size="small" text @click="removeResume">
                <Delete />
                删除
              </el-button>
            </div>
          </div>
        </el-form-item>
        
        <el-form-item class="submit-section">
          <el-button 
            type="primary" 
            size="large" 
            @click="startAnalysis" 
            :loading="loading"
            class="submit-button"
          >
            <MagicStick />
            开始智能分析
          </el-button>
          <p class="submit-hint">分析完成后可直接进入模拟面试环节</p>
        </el-form-item>
      </el-form>
    </div>
    
    <div class="features-section">
      <div class="feature-card">
        <div class="feature-icon blue">
          <Cpu />
        </div>
        <h3>智能JD解析</h3>
        <p>深度分析岗位要求，精准匹配技能需求</p>
      </div>
      
      <div class="feature-card">
        <div class="feature-icon green">
          <TrendCharts />
        </div>
        <h3>能力评估</h3>
        <p>全方位评估简历与岗位的匹配度</p>
      </div>
      
      <div class="feature-card">
        <div class="feature-icon purple">
          <ChatDotRound />
        </div>
        <h3>AI模拟面试</h3>
        <p>真实面试场景模拟，提升应答能力</p>
      </div>
      
      <div class="feature-card">
        <div class="feature-icon orange">
          <Notebook />
        </div>
        <h3>学习笔记</h3>
        <p>生成个性化学习计划，针对性提升</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { 
  Star, Aim, CopyDocument, Upload, Document, Delete, 
  MagicStick, Cpu, TrendCharts, ChatDotRound, Notebook 
} from '@element-plus/icons-vue'

const router = useRouter()

const form = reactive({
  jdContent: '',
  resumeContent: ''
})

const resumeFileName = ref('')
const loading = ref(false)

const handleResumeUpload = (uploadFile) => {
  const reader = new FileReader()
  resumeFileName.value = uploadFile.name
  
  reader.onload = (e) => {
    form.resumeContent = e.target.result
    localStorage.setItem('resumeContent', form.resumeContent)
  }
  
  if (uploadFile.raw) {
    reader.readAsText(uploadFile.raw)
  }
}

const removeResume = () => {
  resumeFileName.value = ''
  form.resumeContent = ''
  localStorage.removeItem('resumeContent')
}

const startAnalysis = async () => {
  if (!form.jdContent.trim()) {
    ElMessage.warning('请输入岗位JD内容')
    return
  }
  
  loading.value = true
  
  try {
    localStorage.setItem('jdContent', form.jdContent)
    router.push('/interview')
  } catch (error) {
    console.error('分析失败:', error)
    ElMessage.error('分析失败，请重试')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.home-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 40px 24px;
}

.hero-section {
  text-align: center;
  margin-bottom: 48px;
  padding: 60px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 28px;
  box-shadow: 0 20px 60px rgba(102, 126, 234, 0.35);
  position: relative;
  overflow: hidden;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -20%;
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 70%);
  border-radius: 50%;
}

.hero-section::after {
  content: '';
  position: absolute;
  bottom: -30%;
  left: -10%;
  width: 200px;
  height: 200px;
  background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
  border-radius: 50%;
}

.hero-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  z-index: 1;
}

.hero-icon {
  width: 96px;
  height: 96px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 32px;
  margin-bottom: 24px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.hero-icon .el-icon {
  font-size: 44px;
  color: #ffffff;
}

.hero-title {
  font-size: clamp(2rem, 5vw, 3rem);
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 16px;
  letter-spacing: -0.3px;
}

.hero-subtitle {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.85);
  max-width: 500px;
  font-weight: 400;
}

.main-card {
  background: #ffffff;
  border-radius: 24px;
  padding: 40px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.06);
  border: 1px solid rgba(0, 0, 0, 0.04);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 18px;
  padding-bottom: 30px;
  border-bottom: 1px solid #f0f0f0;
  margin-bottom: 32px;
}

.header-icon {
  width: 52px;
  height: 52px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #007aff 0%, #5856d6 100%);
  border-radius: 18px;
  box-shadow: 0 4px 16px rgba(0, 122, 255, 0.3);
}

.header-icon .el-icon {
  font-size: 26px;
  color: #ffffff;
}

.header-text h2 {
  font-size: 24px;
  font-weight: 700;
  color: #1d1d1f;
  margin: 0 0 6px 0;
}

.header-text p {
  font-size: 15px;
  color: #6b7280;
  margin: 0;
}

.textarea-wrapper {
  position: relative;
}

.jd-textarea {
  width: 100%;
}

.jd-textarea :deep(.el-textarea__inner) {
  font-size: 15px;
  line-height: 1.7;
  padding: 20px;
  border-radius: 16px;
  border: 2px solid #e5e7eb;
  background: #fafafa;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-family: inherit;
}

.jd-textarea :deep(.el-textarea__inner:focus) {
  border-color: #007aff;
  background: #ffffff;
  box-shadow: 0 0 0 4px rgba(0, 122, 255, 0.1);
  transform: translateY(-1px);
}

.jd-textarea :deep(.el-textarea__inner)::placeholder {
  color: #9ca3af;
}

.textarea-hint {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 12px;
  padding: 12px 16px;
  background: #f9fafb;
  border-radius: 12px;
  font-size: 13px;
  color: #6b7280;
}

.textarea-hint .el-icon {
  font-size: 15px;
  color: #007aff;
}

.upload-wrapper {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.resume-upload {
  width: 100%;
}

.resume-upload :deep(.el-upload-dragger) {
  padding: 56px 24px;
  border: 2px dashed #d1d5db;
  border-radius: 20px;
  background: #fafafa;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.resume-upload :deep(.el-upload-dragger:hover) {
  border-color: #007aff;
  background: #f0f7ff;
  transform: translateY(-2px);
}

.resume-upload :deep(.el-upload-dragger.is-dragover) {
  border-color: #007aff;
  background: #f0f7ff;
  box-shadow: 0 0 0 4px rgba(0, 122, 255, 0.12);
}

.upload-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.upload-icon {
  width: 64px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
  border-radius: 20px;
  transition: all 0.3s ease;
}

.resume-upload :deep(.el-upload-dragger:hover) .upload-icon {
  background: linear-gradient(135deg, rgba(0, 122, 255, 0.1) 0%, rgba(88, 86, 214, 0.1) 100%);
}

.resume-upload :deep(.el-upload-dragger:hover) .upload-icon .el-icon {
  color: #007aff;
}

.upload-icon .el-icon {
  font-size: 32px;
  color: #6b7280;
  transition: all 0.3s ease;
}

.upload-text {
  text-align: center;
}

.upload-text span:first-child {
  display: block;
  font-size: 16px;
  color: #374151;
  font-weight: 600;
  margin-bottom: 8px;
}

.upload-format {
  display: block;
  font-size: 14px;
  color: #9ca3af;
}

.uploaded-file {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: linear-gradient(135deg, rgba(52, 199, 89, 0.08) 0%, rgba(34, 197, 94, 0.08) 100%);
  border: 1px solid rgba(34, 197, 94, 0.25);
  border-radius: 14px;
  transition: all 0.3s ease;
}

.file-info {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #16a34a;
  font-size: 15px;
  font-weight: 500;
}

.file-info .el-icon {
  font-size: 20px;
}

.submit-section {
  margin-top: 32px;
}

.submit-button {
  width: 100%;
  height: 60px;
  font-size: 17px;
  font-weight: 600;
  border-radius: 16px;
  background: linear-gradient(135deg, #007aff 0%, #5856d6 100%);
  border: none;
  box-shadow: 0 6px 20px rgba(0, 122, 255, 0.35);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.submit-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 28px rgba(0, 122, 255, 0.4);
}

.submit-button:active {
  transform: translateY(-1px);
}

.submit-button :deep(.el-icon) {
  margin-right: 10px;
}

.submit-hint {
  text-align: center;
  font-size: 13px;
  color: #9ca3af;
  margin-top: 14px;
}

.features-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 24px;
  margin-top: 50px;
}

.feature-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 32px 24px;
  background: #ffffff;
  border-radius: 20px;
  border: 1px solid #f0f0f0;
  text-align: center;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.feature-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, transparent, #007aff, transparent);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.1);
  border-color: #e5e7eb;
}

.feature-card:hover::before {
  opacity: 1;
}

.feature-icon {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 18px;
  margin-bottom: 18px;
  transition: all 0.3s ease;
}

.feature-card:hover .feature-icon {
  transform: scale(1.1);
}

.feature-icon.blue {
  background: linear-gradient(135deg, rgba(0, 122, 255, 0.12) 0%, rgba(59, 130, 246, 0.12) 100%);
}

.feature-icon.blue .el-icon {
  color: #007aff;
}

.feature-icon.green {
  background: linear-gradient(135deg, rgba(34, 197, 94, 0.12) 0%, rgba(16, 185, 129, 0.12) 100%);
}

.feature-icon.green .el-icon {
  color: #22c55e;
}

.feature-icon.purple {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.12) 0%, rgba(168, 85, 247, 0.12) 100%);
}

.feature-icon.purple .el-icon {
  color: #8b5cf6;
}

.feature-icon.orange {
  background: linear-gradient(135deg, rgba(249, 115, 22, 0.12) 0%, rgba(251, 146, 60, 0.12) 100%);
}

.feature-icon.orange .el-icon {
  color: #f97316;
}

.feature-icon .el-icon {
  font-size: 26px;
}

.feature-card h3 {
  font-size: 16px;
  font-weight: 600;
  color: #1d1d1f;
  margin-bottom: 8px;
}

.feature-card p {
  font-size: 14px;
  color: #6b7280;
  line-height: 1.6;
}

@media (max-width: 768px) {
  .home-container {
    padding: 24px 16px;
  }
  
  .hero-section {
    padding: 40px 20px;
    margin-bottom: 32px;
    border-radius: 20px;
  }
  
  .hero-icon {
    width: 72px;
    height: 72px;
    margin-bottom: 16px;
  }
  
  .hero-icon .el-icon {
    font-size: 32px;
  }
  
  .hero-title {
    font-size: 1.8rem;
  }
  
  .main-card {
    padding: 24px;
  }
  
  .card-header {
    padding-bottom: 20px;
    margin-bottom: 24px;
    gap: 14px;
  }
  
  .header-icon {
    width: 44px;
    height: 44px;
  }
  
  .header-icon .el-icon {
    font-size: 22px;
  }
  
  .header-text h2 {
    font-size: 20px;
  }
  
  .features-section {
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
    margin-top: 32px;
  }
  
  .feature-card {
    padding: 20px 14px;
  }
  
  .feature-icon {
    width: 44px;
    height: 44px;
    margin-bottom: 12px;
  }
  
  .feature-icon .el-icon {
    font-size: 22px;
  }
  
  .feature-card h3 {
    font-size: 15px;
  }
  
  .feature-card p {
    font-size: 13px;
  }
}

@media (max-width: 480px) {
  .hero-section {
    padding: 32px 16px;
  }
  
  .hero-title {
    font-size: 1.5rem;
  }
  
  .main-card {
    padding: 20px;
  }
  
  .features-section {
    grid-template-columns: 1fr;
  }
}
</style>
