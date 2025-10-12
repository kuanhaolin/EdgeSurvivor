# 興趣標籤功能說明

##  功能概述

用戶現在可以設定自己的興趣標籤,並且其他用戶可以在查看資料時看到這些標籤。

---

##  後端實作

### 1. 數據庫變更

**新增欄位**: `users.interests` (TEXT 類型)

```sql
ALTER TABLE users 
ADD COLUMN interests TEXT NULL 
AFTER age;
```

### 2. User 模型更新

**位置**: `backend/models/user.py`

- 添加 `interests` 欄位
- `to_dict()` 方法自動將 JSON 字串轉換為列表返回

```python
# 欄位定義
interests = db.Column(db.Text)

# 自動轉換
interests_list = []
if self.interests:
    try:
        import json
        interests_list = json.loads(self.interests)
    except:
        interests_list = [i.strip() for i in self.interests.split(',') if i.strip()]
```

### 3. API 端點

#### 更新個人資料 (包含興趣)
```http
PUT /api/users/profile
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "小明",
  "interests": ["登山", "攝影", "美食", "旅遊"]
}
```

#### 獲取個人資料
```http
GET /api/users/profile
Authorization: Bearer <token>

Response:
{
  "user": {
    "user_id": 1,
    "name": "小明",
    "interests": ["登山", "攝影", "美食", "旅遊"],
    ...
  }
}
```

#### 查看其他用戶資料
```http
GET /api/users/<user_id>
Authorization: Bearer <token>

Response:
{
  "user": {
    "user_id": 2,
    "name": "小美",
    "interests": ["露營", "烹飪", "閱讀"],
    ...
  }
}
```

---

##  前端實作建議

### 1. Profile 頁面 - 編輯興趣

```vue
<template>
  <el-form-item label="興趣標籤">
    <el-select
      v-model="formData.interests"
      multiple
      filterable
      allow-create
      default-first-option
      placeholder="選擇或輸入你的興趣"
      style="width: 100%"
    >
      <el-option
        v-for="interest in commonInterests"
        :key="interest"
        :label="interest"
        :value="interest"
      />
    </el-select>
  </el-form-item>
</template>

<script setup>
import { ref } from 'vue'

const formData = ref({
  interests: []
})

// 常見興趣選項
const commonInterests = [
  '登山', '露營', '攝影', '美食',
  '旅遊', '閱讀', '電影', '音樂',
  '運動', '健身', '游泳', '跑步',
  '烹飪', '烘焙', '繪畫', '寫作'
]

const updateProfile = async () => {
  try {
    const response = await axios.put('/api/users/profile', {
      ...formData.value,
      interests: formData.value.interests
    })
    ElMessage.success('資料更新成功')
  } catch (error) {
    ElMessage.error('更新失敗')
  }
}
</script>
```

### 2. 顯示用戶興趣標籤

```vue
<template>
  <div class="user-interests">
    <h3>興趣愛好</h3>
    <div class="interest-tags">
      <el-tag
        v-for="interest in user.interests"
        :key="interest"
        type="primary"
        effect="light"
      >
        {{ interest }}
      </el-tag>
    </div>
    <el-empty v-if="!user.interests || user.interests.length === 0" 
              description="尚未設定興趣" />
  </div>
</template>

<style scoped>
.interest-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 12px;
}
</style>
```

### 3. 在聊天/活動詳情中顯示

```vue
<template>
  <el-card class="user-card">
    <div class="user-header">
      <el-avatar :src="user.avatar" :size="60" />
      <div class="user-info">
        <h3>{{ user.name }}</h3>
        <p>{{ user.location }}</p>
      </div>
    </div>
    
    <div class="user-bio">
      {{ user.bio }}
    </div>
    
    <!-- 興趣標籤 -->
    <div v-if="user.interests && user.interests.length > 0" class="user-interests">
      <div class="section-label">興趣愛好</div>
      <div class="interest-tags">
        <el-tag
          v-for="interest in user.interests"
          :key="interest"
          size="small"
          round
        >
          {{ interest }}
        </el-tag>
      </div>
    </div>
  </el-card>
</template>
```

---

##  推薦興趣類別

### 戶外活動
- 登山、露營、健行、攀岩、野營、釣魚

### 運動健身
- 跑步、游泳、瑜伽、健身、騎行、球類運動

### 藝術創作
- 攝影、繪畫、寫作、手工藝、音樂、舞蹈

### 美食探索
- 烹飪、烘焙、咖啡、品酒、探店、各國料理

### 文化娛樂
- 閱讀、電影、展覽、音樂會、戲劇、博物館

### 旅遊冒險
- 自助旅行、背包客、城市探索、文化體驗

---

##  進階功能建議

### 1. 興趣匹配度計算

```javascript
function calculateInterestMatch(userA, userB) {
  const interestsA = new Set(userA.interests || [])
  const interestsB = new Set(userB.interests || [])
  
  const common = [...interestsA].filter(i => interestsB.has(i))
  const total = new Set([...interestsA, ...interestsB]).size
  
  return total > 0 ? (common.length / total * 100).toFixed(0) : 0
}
```

### 2. 按興趣搜索用戶

```python
# 後端 API
@users_bp.route('/search-by-interests', methods=['POST'])
@jwt_required()
def search_by_interests():
    data = request.get_json()
    interests = data.get('interests', [])
    
    users = User.query.all()
    matched_users = []
    
    for user in users:
        if user.interests:
            user_interests = json.loads(user.interests)
            if any(interest in user_interests for interest in interests):
                matched_users.append(user.to_dict())
    
    return jsonify({'users': matched_users}), 200
```

### 3. 熱門興趣標籤統計

```python
@users_bp.route('/popular-interests', methods=['GET'])
def get_popular_interests():
    users = User.query.all()
    interest_count = {}
    
    for user in users:
        if user.interests:
            user_interests = json.loads(user.interests)
            for interest in user_interests:
                interest_count[interest] = interest_count.get(interest, 0) + 1
    
    # 排序並返回前 20 個
    popular = sorted(interest_count.items(), key=lambda x: x[1], reverse=True)[:20]
    
    return jsonify({
        'interests': [{'name': k, 'count': v} for k, v in popular]
    }), 200
```

---

##  測試清單

- [ ] 添加興趣標籤
- [ ] 修改興趣標籤
- [ ] 刪除興趣標籤
- [ ] 查看自己的興趣
- [ ] 查看其他用戶的興趣
- [ ] 興趣標籤顯示正常
- [ ] 空興趣時顯示提示
- [ ] 多語言興趣支援
- [ ] 特殊字符處理

---

##  使用示例

### 更新興趣標籤

```javascript
// 使用 axios
const updateInterests = async () => {
  try {
    const response = await axios.put('/api/users/profile', {
      interests: ['登山', '攝影', '美食', '旅遊', '閱讀']
    }, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    console.log('更新成功:', response.data)
  } catch (error) {
    console.error('更新失敗:', error)
  }
}
```

### 獲取用戶資料（含興趣）

```javascript
const getUserProfile = async (userId) => {
  try {
    const response = await axios.get(`/api/users/${userId}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    const user = response.data.user
    console.log('用戶興趣:', user.interests)
    // ['登山', '攝影', '美食']
  } catch (error) {
    console.error('獲取失敗:', error)
  }
}
```

---

##  應用場景

1. **個人資料頁**: 展示用戶興趣,讓其他人更了解你
2. **活動配對**: 根據興趣推薦相關活動
3. **用戶匹配**: 找到興趣相投的旅伴
4. **聊天介面**: 在聊天時顯示對方興趣,作為話題起點
5. **搜索過濾**: 按興趣搜索志同道合的用戶

---

##  後續優化

1. **興趣分類**: 將興趣分為不同類別（運動、藝術、美食等）
2. **興趣等級**: 允許用戶標記興趣的熟練度或喜好程度
3. **推薦系統**: 根據興趣推薦活動和用戶
4. **數據分析**: 統計最熱門的興趣標籤
5. **社群功能**: 創建基於興趣的討論群組

---

完成! 
