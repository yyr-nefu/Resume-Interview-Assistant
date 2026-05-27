<template>
  <div class="review-container">
    <div class="section-header">
      <h2>面试复盘</h2>
      <p>双维度评分，提供优化建议</p>
    </div>
    
    <div class="main-content" v-if="result">
      <div class="scores-section">
        <div class="score-card professional">
          <div class="score-icon">
            <Trophy :size="48" />
          </div>
          <div class="score-info">
            <div class="score-value">{{ result.professional_score }}</div>
            <div class="score-label">专业性得分</div>
          </div>
        </div>
        <div class="score-card comprehensive">
          <div class="score-icon">
            <Grid :size="48" />
          </div>
          <div class="score-info">
            <div class="score-value">{{ result.comprehensive_score }}</div>
            <div class="score-label">全面性得分</div>
          </div>
        </div>
      </div>
      
      <div class="details-section">
        <el-card title="答题详情">
          <div class="review-item" v-for="review in result.reviews" :key="review.question_id">
            <div class="question-header">
              <span class="question-number">问题 {{ review.question_id }}</span>
              <el-tag :type="getScoreType(review.score)">{{ review.score }} 分</el-tag>
            </div>
            <div class="question-text">{{ review.question }}</div>
            <div class="answer-box">
              <span class="label">你的回答：</span>
              <p>{{ review.answer }}</p>
            </div>
            <div class="feedback-box">
              <span class="label">点评：</span>
              <p>{{ review.feedback }}</p>
            </div>
            <div class="keyword-box" v-if="review.keyword_matches.length > 0">
              <span class="label">命中关键词：</span>
              <el-tag v-for="kw in review.keyword_matches" :key="kw">{{ kw }}</el-tag>
            </div>
          </div>
        </el-card>
        
        <el-card title="答题模板">
          <ul class="template-list">
            <li v-for="(template, index) in result.templates" :key="index">
              <CollectionTag />
              {{ template }}
            </li>
          </ul>
        </el-card>
        
        <el-card title="优秀回答范例">
          <ul class="example-list">
            <li v-for="(example, index) in result.examples" :key="index">
              <Star />
              {{ example }}
            </li>
          </ul>
        </el-card>
      </div>
      
      <div class="action-buttons">
        <el-button type="primary" @click="goToNotes">
          <Memo />
          生成学习笔记
        </el-button>
        <el-button @click="goToInterview">
          <Refresh />
          再次面试
        </el-button>
        <el-button @click="goToArchive">
          <FolderOpened />
          查看归档
        </el-button>
      </div>
    </div>
    
    <div class="loading-section" v-else>
      <el-spinner size="large" />
      <p>正在生成复盘报告...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'
import { Trophy, Grid, CollectionTag, Star, Memo, Refresh, FolderOpened } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()

const result = ref(null)

const getScoreType = (score) => {
  if (score >= 80) return 'success'
  if (score >= 60) return 'warning'
  return 'danger'
}

onMounted(async () => {
  const sessionId = route.params.sessionId
  try {
    const response = await axios.post('/api/interview/complete', {
      session_id: sessionId
    })
    result.value = response.data
    localStorage.setItem('lastReview', JSON.stringify(response.data))
  } catch (error) {
    console.error('获取复盘失败:', error)
    alert('获取复盘失败，请重试')
  }
})

const goToNotes = () => {
  router.push('/notes')
}

const goToInterview = () => {
  router.push('/interview')
}

const goToArchive = () => {
  router.push('/archive')
}
</script>

<style scoped>
.review-container {
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

.scores-section {
  display: flex;
  gap: 16px;
  margin-bottom: 20px;
}

.score-card {
  flex: 1;
  background: #ffffff;
  border: 1px solid #e8e8e8;
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.score-icon {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.professional .score-icon {
  background: linear-gradient(135deg, #007aff 0%, #5856d6 100%);
  color: white;
}

.comprehensive .score-icon {
  background: linear-gradient(135deg, #ff9500 0%, #ff2d55 100%);
  color: white;
}

.score-value {
  font-size: 42px;
  font-weight: 600;
  color: #1d1d1f;
}

.score-label {
  color: #86868b;
  font-size: 13px;
}

.details-section {
  display: grid;
  gap: 20px;
}

.details-section :deep(.el-card) {
  background: #ffffff;
  border: 1px solid #e8e8e8;
  border-radius: 16px;
}

.details-section :deep(.el-card__header) {
  border-bottom: 1px solid #e8e8e8;
  color: #1d1d1f;
  font-weight: 600;
}

.review-item {
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e8e8e8;
}

.review-item:last-child {
  border-bottom: none;
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.question-number {
  font-weight: 600;
  color: #007aff;
  font-size: 14px;
}

.question-text {
  font-size: 15px;
  margin-bottom: 14px;
  padding: 14px;
  background: #f5f5f7;
  border-radius: 8px;
  color: #1d1d1f;
  line-height: 1.6;
}

.answer-box, .feedback-box {
  margin-bottom: 12px;
}

.answer-box .label, .feedback-box .label {
  font-weight: 500;
  color: #333333;
  font-size: 14px;
}

.answer-box p, .feedback-box p {
  margin-top: 6px;
  padding: 12px;
  background: #fafafa;
  border: 1px solid #e8e8e8;
  border-radius: 8px;
  color: #333333;
  font-size: 14px;
  line-height: 1.6;
}

.keyword-box {
  margin-top: 12px;
}

.keyword-box .label {
  font-weight: 500;
  color: #333333;
  font-size: 14px;
}

.template-list, .example-list {
  padding-left: 20px;
}

.template-list li, .example-list li {
  margin-bottom: 8px;
  padding: 12px;
  background: #f5f5f7;
  border-radius: 8px;
  color: #333333;
  font-size: 13px;
}

.action-buttons {
  margin-top: 24px;
  display: flex;
  gap: 10px;
  justify-content: center;
}

.loading-section {
  text-align: center;
  padding: 60px;
  color: white;
}
</style>