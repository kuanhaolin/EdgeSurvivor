<template>
  <div class="expense-container">
    <!-- 費用總覽 -->
    <el-row :gutter="20" class="summary-row">
      <el-col :span="8">
        <el-statistic title="總費用" :value="summary.total_amount || 0" prefix="$" />
      </el-col>
      <el-col :span="8">
        <el-statistic title="參與人數" :value="summary.participant_count || 0" suffix="人" />
      </el-col>
      <el-col :span="8">
        <el-statistic title="每人平均" :value="summary.per_person || 0" prefix="$" />
      </el-col>
    </el-row>
    
    <!-- 費用列表 -->
    <el-card class="expense-list-card">
      <template #header>
        <div class="card-header">
          <span>費用明細</span>
          <el-button type="primary" @click="showAddDialog = true">
            <el-icon><Plus /></el-icon>
            新增費用
          </el-button>
        </div>
      </template>
      
      <el-table :data="expenses" stripe>
        <el-table-column label="日期" width="120">
          <template #default="scope">
            {{ formatDate(scope.row.expense_date) }}
          </template>
        </el-table-column>
        <el-table-column label="類別" width="100">
          <template #default="scope">
            <el-tag :type="getCategoryType(scope.row.category)">
              {{ getCategoryText(scope.row.category) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="項目" prop="description" />
        <el-table-column label="金額" width="120" align="right">
          <template #default="scope">
            <strong>$ {{ scope.row.amount }}</strong>
          </template>
        </el-table-column>
        <el-table-column label="付款者" width="120">
          <template #default="scope">
            {{ scope.row.payer?.name }}
          </template>
        </el-table-column>
        <el-table-column label="分攤" width="100" align="center">
          <template #default="scope">
            <el-tag v-if="scope.row.is_split" type="success" size="small">
              平均分攤
            </el-tag>
            <el-tag v-else type="info" size="small">
              個人支出
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100" align="center">
          <template #default="scope">
            <el-button
              v-if="canDelete(scope.row)"
              type="danger"
              size="small"
              text
              @click="deleteExpense(scope.row.expense_id)"
            >
              刪除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <el-empty v-if="expenses.length === 0" description="還沒有費用記錄">
        <el-button type="primary" @click="showAddDialog = true">新增第一筆費用</el-button>
      </el-empty>
    </el-card>
    
    <!-- 費用結算 -->
    <el-card v-if="settlements.length > 0" class="settlement-card">
      <template #header>
        <div class="card-header">
          <span>💰 費用結算</span>
          <el-button size="small" @click="loadSettlement">
            <el-icon><Refresh /></el-icon>
            重新計算
          </el-button>
        </div>
      </template>
      
      <el-alert
        title="結算說明"
        description="以下為最優化的付款方案，可以用最少的轉賬次數完成費用結算"
        type="info"
        :closable="false"
        show-icon
      />
      
      <div class="settlement-list">
        <div
          v-for="(settlement, index) in settlements"
          :key="`${settlement.from_user_id}-${settlement.to_user_id}`"
          class="settlement-item"
        >
          <el-tag size="large" type="warning">
            {{ settlement.from_user_name }}
          </el-tag>
          <el-icon><Right /></el-icon>
          <span class="settlement-text">應付給</span>
          <el-icon><Right /></el-icon>
          <el-tag size="large" type="success">
            {{ settlement.to_user_name }}
          </el-tag>
          <el-divider direction="vertical" />
          <strong class="settlement-amount">$ {{ settlement.amount }}</strong>
        </div>
      </div>
    </el-card>
    
    <!-- 新增費用對話框 -->
    <el-dialog v-model="showAddDialog" title="新增費用" width="500px">
      <el-form :model="expenseForm" label-width="100px">
        <el-form-item label="費用項目" required>
          <el-input v-model="expenseForm.description" placeholder="例如：午餐費用" />
        </el-form-item>
        
        <el-form-item label="金額" required>
          <el-input-number
            v-model="expenseForm.amount"
            :min="0"
            :precision="0"
            placeholder="0"
          />
        </el-form-item>
        
        <el-form-item label="類別" required>
          <el-select v-model="expenseForm.category" placeholder="請選擇">
            <el-option label="交通" value="transport" />
            <el-option label="住宿" value="accommodation" />
            <el-option label="餐飲" value="food" />
            <el-option label="門票" value="ticket" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="費用日期">
          <el-date-picker
            v-model="expenseForm.expense_date"
            type="date"
            placeholder="選擇日期"
            style="width: 100%"
          />
        </el-form-item>
        
        <el-form-item label="分攤方式">
          <el-radio-group v-model="expenseForm.is_split">
            <el-radio :label="true">所有人平均分攤</el-radio>
            <el-radio :label="false">個人支出（不分攤）</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="showAddDialog = false">取消</el-button>
        <el-button type="primary" @click="addExpense">新增</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Refresh, Right } from '@element-plus/icons-vue'
import axios from '@/utils/axios'

const props = defineProps({
  activityId: {
    type: Number,
    required: true
  },
  creatorId: {
    type: Number,
    required: false
  }
})

const expenses = ref([])
const summary = ref({
  total_amount: 0,
  participant_count: 0,
  per_person: 0
})
const settlements = ref([])
const showAddDialog = ref(false)

const expenseForm = reactive({
  description: '',
  amount: 0,
  category: '',
  expense_date: new Date(),
  is_split: true,
  split_method: 'equal'
})

const currentUserId = computed(() => {
  const user = JSON.parse(localStorage.getItem('user') || '{}')
  return user.user_id
})

// 載入費用列表
const loadExpenses = async () => {
  try {
    const response = await axios.get(`/activities/${props.activityId}/expenses`)
    expenses.value = response.data.expenses || []
    summary.value = response.data.summary || {
      total_amount: 0,
      participant_count: 0,
      per_person: 0
    }
  } catch (error) {
    console.error('載入費用失敗:', error)
    ElMessage.error('載入費用失敗')
  }
}

// 載入結算
const loadSettlement = async () => {
  try {
    const response = await axios.get(`/activities/${props.activityId}/expenses/settlement`)
    settlements.value = response.data.settlements || []
  } catch (error) {
    console.error('載入結算失敗:', error)
    if (error.response?.status !== 404) {
      ElMessage.error('載入結算失敗')
    }
  }
}

// 新增費用
const addExpense = async () => {
  if (!expenseForm.description || !expenseForm.amount || !expenseForm.category) {
    ElMessage.error('請填寫所有必填欄位')
    return
  }
  
  try {
    await axios.post(`/activities/${props.activityId}/expenses`, {
      description: expenseForm.description,
      amount: expenseForm.amount,
      category: expenseForm.category,
      expense_date: expenseForm.expense_date,
      is_split: expenseForm.is_split,
      split_method: expenseForm.split_method
    })
    
    ElMessage.success('費用已新增')
    showAddDialog.value = false
    
    // 重置表單
    expenseForm.description = ''
    expenseForm.amount = 0
    expenseForm.category = ''
    expenseForm.expense_date = new Date()
    expenseForm.is_split = true
    
    // 重新載入
    await loadExpenses()
    await loadSettlement()
  } catch (error) {
    console.error('新增費用失敗:', error)
    ElMessage.error(error.response?.data?.error || '新增費用失敗')
  }
}

// 刪除費用
const deleteExpense = async (expenseId) => {
  try {
    await ElMessageBox.confirm('確定要刪除這筆費用嗎？', '確認', {
      confirmButtonText: '確定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await axios.delete(`/expenses/${expenseId}`)
    ElMessage.success('費用已刪除')
    
    await loadExpenses()
    await loadSettlement()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('刪除費用失敗:', error)
      ElMessage.error(error.response?.data?.error || '刪除費用失敗')
    }
  }
}

// 判斷是否可以刪除
const canDelete = (expense) => {
  return expense.payer_id === currentUserId.value || currentUserId.value === props.creatorId
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleDateString('zh-TW')
}

// 獲取類別標籤類型
const getCategoryType = (category) => {
  const types = {
    transport: 'primary',
    accommodation: 'success',
    food: 'warning',
    ticket: 'danger',
    other: 'info'
  }
  return types[category] || 'info'
}

// 獲取類別文字
const getCategoryText = (category) => {
  const texts = {
    transport: '交通',
    accommodation: '住宿',
    food: '餐飲',
    ticket: '門票',
    other: '其他'
  }
  return texts[category] || category
}

// 組件掛載時載入數據
onMounted(() => {
  loadExpenses()
  loadSettlement()
})
</script>

<style scoped>
.expense-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.summary-row {
  margin-bottom: 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.expense-list-card,
.settlement-card {
  margin-top: 0;
}

.settlement-list {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.settlement-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 8px;
  font-size: 14px;
}

.settlement-text {
  color: #606266;
  font-weight: 500;
}

.settlement-amount {
  color: #f56c6c;
  font-size: 18px;
}

.el-statistic {
  text-align: center;
}
</style>
