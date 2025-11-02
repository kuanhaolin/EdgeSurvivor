<template>
  <div class="profile">
    <NavBar />
    
    <div class="profile-container">
      <el-page-header @back="goBack" content="個人資料" />
      
      <el-row :gutter="20" class="profile-row">
        <!-- 左側個人資訊卡片 -->
        <el-col :xs="24" :md="8">
          <el-card class="profile-card">
            <div class="avatar-section">
              <el-avatar :size="120" :src="userProfile.avatar" />
              <el-button type="primary" size="small" class="upload-btn" @click="uploadAvatar">
                <el-icon><Upload /></el-icon>
                更換頭像
              </el-button>
              <!-- 隱藏的文件輸入 -->
              <input
                ref="avatarInput"
                type="file"
                accept="image/*"
                style="display: none"
                @change="handleAvatarUpload"
              />
            </div>
            
            <div class="user-basic-info">
              <h2>{{ userProfile.name }}</h2>
              <el-tag v-if="userProfile.verified" type="success">
                <el-icon><Select /></el-icon>
                已驗證
              </el-tag>
              <el-tag v-else type="info">未驗證</el-tag>
            </div>
            
            <el-descriptions :column="1" border class="user-details">
              <el-descriptions-item label="電子郵件">
                {{ userProfile.email }}
              </el-descriptions-item>
              <el-descriptions-item label="性別">
                {{ getGenderText(userProfile.gender) }}
              </el-descriptions-item>
              <el-descriptions-item label="年齡">
                {{ userProfile.age }} 歲
              </el-descriptions-item>
              <el-descriptions-item label="地區">
                {{ userProfile.location || '未設定' }}
              </el-descriptions-item>
              <el-descriptions-item label="加入時間">
                {{ userProfile.joinDate }}
              </el-descriptions-item>
            </el-descriptions>
            
            <div class="profile-stats">
              <div class="stat-item">
                <div class="stat-value">{{ userProfile.stats.activities }}</div>
                <div class="stat-label">活動</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">{{ userProfile.stats.matches }}</div>
                <div class="stat-label">好友</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">{{ userProfile.stats.reviews }}</div>
                <div class="stat-label">評價</div>
              </div>
            </div>
            
            <!-- 社群帳號展示 -->
            <el-divider content-position="center">
              <span style="color: #909399; font-size: 14px;">社群帳號</span>
            </el-divider>
            <div class="social-links-display">
              <el-button
                v-if="socialLinks.instagram"
                circle
                size="large"
                style="background: linear-gradient(45deg, #f09433 0%,#e6683c 25%,#dc2743 50%,#cc2366 75%,#bc1888 100%); color: white; border: none;"
                @click="openSocialLink(socialLinks.instagram)"
                title="Instagram"
              >
                <el-icon :size="20"><svg viewBox="0 0 24 24"><path fill="currentColor" d="M7.8,2H16.2C19.4,2 22,4.6 22,7.8V16.2A5.8,5.8 0 0,1 16.2,22H7.8C4.6,22 2,19.4 2,16.2V7.8A5.8,5.8 0 0,1 7.8,2M7.6,4A3.6,3.6 0 0,0 4,7.6V16.4C4,18.39 5.61,20 7.6,20H16.4A3.6,3.6 0 0,0 20,16.4V7.6C20,5.61 18.39,4 16.4,4H7.6M17.25,5.5A1.25,1.25 0 0,1 18.5,6.75A1.25,1.25 0 0,1 17.25,8A1.25,1.25 0 0,1 16,6.75A1.25,1.25 0 0,1 17.25,5.5M12,7A5,5 0 0,1 17,12A5,5 0 0,1 12,17A5,5 0 0,1 7,12A5,5 0 0,1 12,7M12,9A3,3 0 0,0 9,12A3,3 0 0,0 12,15A3,3 0 0,0 15,12A3,3 0 0,0 12,9Z" /></svg></el-icon>
              </el-button>
              
              <el-button
                v-if="socialLinks.facebook"
                circle
                size="large"
                style="background: #1877F2; color: white; border: none;"
                @click="openSocialLink(socialLinks.facebook)"
                title="Facebook"
              >
                <el-icon :size="20"><svg viewBox="0 0 24 24"><path fill="currentColor" d="M12 2.04C6.5 2.04 2 6.53 2 12.06C2 17.06 5.66 21.21 10.44 21.96V14.96H7.9V12.06H10.44V9.85C10.44 7.34 11.93 5.96 14.22 5.96C15.31 5.96 16.45 6.15 16.45 6.15V8.62H15.19C13.95 8.62 13.56 9.39 13.56 10.18V12.06H16.34L15.89 14.96H13.56V21.96A10 10 0 0 0 22 12.06C22 6.53 17.5 2.04 12 2.04Z" /></svg></el-icon>
              </el-button>
              
              <el-button
                v-if="socialLinks.line"
                circle
                size="large"
                style="background: #00B900; color: white; border: none;"
                @click="showLineQRCode"
                title="LINE (點擊顯示 QR Code)"
              >
                <el-icon :size="20"><svg viewBox="0 0 24 24"><path fill="currentColor" d="M19.365,9.863c.349,0,.698.025,1.041.083,0-5.094-5.098-9.233-11.381-9.233C3.75.713,0,4.853,0,9.948s3.75,9.235,8.988,9.235c1.031,0,2.025-.149,2.949-.43L19.373,24V18.048a6.644,6.644,0,0,0,2.065-4.784A6.618,6.618,0,0,0,19.365,9.863Z" /></svg></el-icon>
              </el-button>
              
              <el-button
                v-if="socialLinks.twitter"
                circle
                size="large"
                style="background: #000000; color: white; border: none;"
                @click="openSocialLink(socialLinks.twitter)"
                title="Twitter (X)"
              >
                <el-icon :size="20"><svg viewBox="0 0 24 24"><path fill="currentColor" d="M22.46,6C21.69,6.35 20.86,6.58 20,6.69C20.88,6.16 21.56,5.32 21.88,4.31C21.05,4.81 20.13,5.16 19.16,5.36C18.37,4.5 17.26,4 16,4C13.65,4 11.73,5.92 11.73,8.29C11.73,8.63 11.77,8.96 11.84,9.27C8.28,9.09 5.11,7.38 3,4.79C2.63,5.42 2.42,6.16 2.42,6.94C2.42,8.43 3.17,9.75 4.33,10.5C3.62,10.5 2.96,10.3 2.38,10C2.38,10 2.38,10 2.38,10.03C2.38,12.11 3.86,13.85 5.82,14.24C5.46,14.34 5.08,14.39 4.69,14.39C4.42,14.39 4.15,14.36 3.89,14.31C4.43,16 6,17.26 7.89,17.29C6.43,18.45 4.58,19.13 2.56,19.13C2.22,19.13 1.88,19.11 1.54,19.07C3.44,20.29 5.70,21 8.12,21C16,21 20.33,14.46 20.33,8.79C20.33,8.6 20.33,8.42 20.32,8.23C21.16,7.63 21.88,6.87 22.46,6Z" /></svg></el-icon>
              </el-button>
              
              <div v-if="!socialLinks.instagram && !socialLinks.facebook && !socialLinks.line && !socialLinks.twitter" style="color: #909399; font-size: 14px; text-align: center; padding: 10px;">
                未公開/未綁定社群帳號
              </div>
            </div>
          </el-card>
        </el-col>
        
        <!-- 右側編輯區域 -->
        <el-col :xs="24" :md="16">
          <el-tabs v-model="activeTab">
            <!-- 基本資料 -->
            <el-tab-pane label="基本資料" name="basic">
              <el-card>
                <el-form :model="editForm" label-width="100px">
                  <el-form-item label="姓名">
                    <el-input v-model="editForm.name" />
                  </el-form-item>
                  
                  <el-form-item label="性別">
                    <el-select v-model="editForm.gender" placeholder="請選擇">
                      <el-option label="男性" value="male" />
                      <el-option label="女性" value="female" />
                      <el-option label="其他" value="other" />
                    </el-select>
                  </el-form-item>
                  
                  <el-form-item label="年齡">
                    <el-input-number v-model="editForm.age" :min="18" :max="100" />
                  </el-form-item>
                  
                  <el-form-item label="地區">
                    <el-cascader
                      v-model="selectedLocation"
                      :options="locationOptions"
                      :props="cascaderProps"
                      placeholder="請選擇國家和城市"
                      style="width: 100%"
                      @change="handleLocationChange"
                      filterable
                    />
                  </el-form-item>
                  
                  <el-form-item label="個人簡介">
                    <el-input
                      v-model="editForm.bio"
                      type="textarea"
                      :rows="4"
                      placeholder="介紹一下自己..."
                    />
                  </el-form-item>
                  
                  <el-form-item label="興趣標籤">
                    <el-tag
                      v-for="tag in editForm.interests"
                      :key="tag"
                      closable
                      @close="removeInterest(tag)"
                      style="margin-right: 8px; margin-bottom: 8px;"
                    >
                      {{ tag }}
                    </el-tag>
                    <el-input
                      v-if="showInterestInput"
                      v-model="newInterest"
                      size="small"
                      style="width: 100px;"
                      @blur="addInterest"
                      @keyup.enter="addInterest"
                    />
                    <el-button v-else size="small" @click="showInterestInput = true">
                      + 新增標籤
                    </el-button>
                  </el-form-item>
                  
                  <el-form-item>
                    <el-button type="primary" @click="saveProfile">儲存變更</el-button>
                    <el-button @click="cancelEdit">取消</el-button>
                  </el-form-item>
                </el-form>
              </el-card>
            </el-tab-pane>
            
            <!-- 社群帳號綁定 -->
            <el-tab-pane label="社群帳號" name="social">
              <el-card>
                <!-- <div class="social-binding-header">
                  <el-icon :size="24" color="#409eff"><Link /></el-icon>
                  <div>
                    <h3>綁定社群帳號</h3>
                    <p>提升個人資料可信度，讓其他旅伴更容易認識您</p>
                  </div>
                </div> -->
                
                <el-form label-width="0px" class="social-form">
                  <!-- Instagram -->
                  <div class="social-input-group instagram-group">
                    <div class="social-label">
                      <div class="social-icon instagram-icon">
                        <svg viewBox="0 0 24 24"><path fill="currentColor" d="M7.8,2H16.2C19.4,2 22,4.6 22,7.8V16.2A5.8,5.8 0 0,1 16.2,22H7.8C4.6,22 2,19.4 2,16.2V7.8A5.8,5.8 0 0,1 7.8,2M7.6,4A3.6,3.6 0 0,0 4,7.6V16.4C4,18.39 5.61,20 7.6,20H16.4A3.6,3.6 0 0,0 20,16.4V7.6C20,5.61 18.39,4 16.4,4H7.6M17.25,5.5A1.25,1.25 0 0,1 18.5,6.75A1.25,1.25 0 0,1 17.25,8A1.25,1.25 0 0,1 16,6.75A1.25,1.25 0 0,1 17.25,5.5M12,7A5,5 0 0,1 17,12A5,5 0 0,1 12,17A5,5 0 0,1 7,12A5,5 0 0,1 12,7M12,9A3,3 0 0,0 9,12A3,3 0 0,0 12,15A3,3 0 0,0 15,12A3,3 0 0,0 12,9Z"></path></svg>
                      </div>
                      <span>Instagram</span>
                    </div>
                    <el-input 
                      v-model="socialLinks.instagram" 
                      placeholder="https://instagram.com/your_username"
                      size="large"
                      clearable
                    />
                    <el-button 
                      v-if="socialLinks.instagram"
                      class="visit-btn"
                      @click="openSocialLink(socialLinks.instagram)"
                      circle
                    >
                      <el-icon><Right /></el-icon>
                    </el-button>
                  </div>
                  
                  <!-- Facebook -->
                  <div class="social-input-group facebook-group">
                    <div class="social-label">
                      <div class="social-icon facebook-icon">
                        <svg viewBox="0 0 24 24"><path fill="currentColor" d="M12 2.04C6.5 2.04 2 6.53 2 12.06C2 17.06 5.66 21.21 10.44 21.96V14.96H7.9V12.06H10.44V9.85C10.44 7.34 11.93 5.96 14.22 5.96C15.31 5.96 16.45 6.15 16.45 6.15V8.62H15.19C13.95 8.62 13.56 9.39 13.56 10.18V12.06H16.34L15.89 14.96H13.56V21.96A10 10 0 0 0 22 12.06C22 6.53 17.5 2.04 12 2.04Z"></path></svg>
                      </div>
                      <span>Facebook</span>
                    </div>
                    <el-input 
                      v-model="socialLinks.facebook" 
                      placeholder="https://facebook.com/your_profile"
                      size="large"
                      clearable
                    />
                    <el-button 
                      v-if="socialLinks.facebook"
                      class="visit-btn"
                      @click="openSocialLink(socialLinks.facebook)"
                      circle
                    >
                      <el-icon><Right /></el-icon>
                    </el-button>
                  </div>
                  
                  <!-- LINE ID -->
                  <div class="social-input-group line-group">
                    <div class="social-label">
                      <div class="social-icon line-icon">
                        <svg viewBox="0 0 24 24"><path fill="currentColor" d="M19.365,9.863c.349,0,.698.025,1.041.083,0-5.094-5.098-9.233-11.381-9.233C3.75.713,0,4.853,0,9.948s3.75,9.235,8.988,9.235c1.031,0,2.025-.149,2.949-.43L19.373,24V18.048a6.644,6.644,0,0,0,2.065-4.784A6.618,6.618,0,0,0,19.365,9.863Z"></path></svg>
                      </div>
                      <span>LINE</span>
                    </div>
                    <el-input 
                      v-model="socialLinks.line" 
                      placeholder="your_line_id"
                      size="large"
                      clearable
                    />
                    <el-button 
                      v-if="socialLinks.line"
                      class="visit-btn"
                      @click="showLineQRCode"
                      circle
                    >
                      <el-icon><Connection /></el-icon>
                    </el-button>
                    <div class="input-hint">
                      <el-icon><InfoFilled /></el-icon>
                      輸入您的 LINE ID，其他用戶可以掃描 QR Code 加您好友
                    </div>
                  </div>
                  
                  <!-- Twitter -->
                  <div class="social-input-group twitter-group">
                    <div class="social-label">
                      <div class="social-icon twitter-icon">
                        <svg viewBox="0 0 24 24"><path fill="currentColor" d="M22.46,6C21.69,6.35 20.86,6.58 20,6.69C20.88,6.16 21.56,5.32 21.88,4.31C21.05,4.81 20.13,5.16 19.16,5.36C18.37,4.5 17.26,4 16,4C13.65,4 11.73,5.92 11.73,8.29C11.73,8.63 11.77,8.96 11.84,9.27C8.28,9.09 5.11,7.38 3,4.79C2.63,5.42 2.42,6.16 2.42,6.94C2.42,8.43 3.17,9.75 4.33,10.5C3.62,10.5 2.96,10.3 2.38,10C2.38,10 2.38,10 2.38,10.03C2.38,12.11 3.86,13.85 5.82,14.24C5.46,14.34 5.08,14.39 4.69,14.39C4.42,14.39 4.15,14.36 3.89,14.31C4.43,16 6,17.26 7.89,17.29C6.43,18.45 4.58,19.13 2.56,19.13C2.22,19.13 1.88,19.11 1.54,19.07C3.44,20.29 5.70,21 8.12,21C16,21 20.33,14.46 20.33,8.79C20.33,8.6 20.33,8.42 20.32,8.23C21.16,7.63 21.88,6.87 22.46,6Z"></path></svg>
                      </div>
                      <span>Twitter (X)</span>
                    </div>
                    <el-input 
                      v-model="socialLinks.twitter" 
                      placeholder="https://twitter.com/your_username"
                      size="large"
                      clearable
                    />
                    <el-button 
                      v-if="socialLinks.twitter"
                      class="visit-btn"
                      @click="openSocialLink(socialLinks.twitter)"
                      circle
                    >
                      <el-icon><Right /></el-icon>
                    </el-button>
                  </div>
                  
                  <div class="form-actions">
                    <el-button type="primary" size="large" @click="saveSocialLinks">儲存變更</el-button>
                    <el-button size="large" @click="cancelSocialEdit">取消</el-button>
                  </div>
                </el-form>
              </el-card>
            </el-tab-pane>
            
            <!-- 隱私設定 -->
            <el-tab-pane label="隱私設定" name="privacy">
              <el-card>
                <el-form label-width="150px">
                  <!-- <el-form-item label="個人資料可見性">
                    <el-radio-group v-model="privacySettings.profileVisibility">
                      <el-radio label="public">公開</el-radio>
                      <el-radio label="partial">部分公開</el-radio>
                      <el-radio label="private">僅自己可見</el-radio>
                    </el-radio-group>
                  </el-form-item>
                  
                  <el-divider content-position="center">
                    <span style="font-size: 14px; color: #606266;"></span>
                  </el-divider> -->
                  
                  <el-form-item label="社群帳號可見性">
                    <el-radio-group v-model="privacySettings.socialPrivacy">
                      <el-radio label="public">
                        <span>所有人可見</span>
                        <!-- <div style="font-size: 12px; color: #909399; margin-top: 4px;">
                          所有用戶都可以看到你的社群帳號連結
                        </div> -->
                      </el-radio>
                      <el-radio label="friends_only">
                        <span>僅好友可見</span>
                        <!-- <div style="font-size: 12px; color: #909399; margin-top: 4px;">
                          只有已成為好友的用戶可以看到你的社群帳號連結
                        </div> -->
                      </el-radio>
                    </el-radio-group>
                    <div style="margin-top: 10px; padding: 10px; background: #f4f4f5; border-radius: 4px; font-size: 13px; color: #606266;">
                      <el-icon style="vertical-align: middle;"><InfoFilled /></el-icon>
                      提示：此設定會影響你的 Instagram、Facebook、LINE 和 Twitter 帳號是否對他人顯示
                    </div>
                  </el-form-item>
                  
                  <el-divider />
                  
                  <!-- <el-form-item label="顯示年齡">
                    <el-switch v-model="privacySettings.showAge" />
                  </el-form-item>
                  
                  <el-form-item label="顯示地區">
                    <el-switch v-model="privacySettings.showLocation" />
                  </el-form-item>
                  
                  <el-form-item label="允許陌生人訊息">
                    <el-switch v-model="privacySettings.allowStrangerMessages" />
                  </el-form-item> -->
                  
                  <el-form-item>
                    <el-button type="primary" @click="savePrivacySettings">儲存設定</el-button>
                  </el-form-item>
                </el-form>
              </el-card>
            </el-tab-pane>
            
            <!-- 帳號安全 -->
            <el-tab-pane label="帳號安全" name="security">
              <el-card>
                <el-form label-width="120px">
                  <el-form-item label="電子郵件">
                    <el-input v-model="userProfile.email" disabled />
                    <el-button type="text" @click="changeEmail">更改電子郵件</el-button>
                  </el-form-item>
                  
                  <el-divider />
                  
                  <el-form-item label="變更密碼">
                    <el-button @click="showPasswordDialog = true">變更密碼</el-button>
                  </el-form-item>
                  
                  <el-divider />
                  
                  <el-form-item label="兩步驟驗證">
                    <el-switch 
                      v-model="securitySettings.twoFactorAuth" 
                      @change="handleTwoFactorChange"
                      :disabled="twoFactorLoading"
                    />
                    <div style="margin-top: 8px; color: #909399; font-size: 12px;">
                      {{ securitySettings.twoFactorAuth ? '已啟用 - 登入時需要輸入驗證碼' : '未啟用 - 建議啟用以提高帳號安全性' }}
                    </div>
                  </el-form-item>
                  
                  <el-divider />
                  
                  <el-form-item label="刪除帳號">
                    <el-button type="danger" @click="deleteAccount">刪除帳號</el-button>
                    <div style="margin-top: 8px; color: #f56c6c; font-size: 12px;">
                      <!-- 刪除後將無法恢復 -->
                    </div>
                  </el-form-item>
                </el-form>
              </el-card>
            </el-tab-pane>
          </el-tabs>
        </el-col>
      </el-row>
    </div>
    
    <!-- 變更密碼對話框 -->
    <el-dialog v-model="showPasswordDialog" title="變更密碼" width="500px">
      <el-form :model="passwordForm" label-width="100px">
        <el-form-item label="目前密碼">
          <el-input v-model="passwordForm.currentPassword" type="password" show-password />
        </el-form-item>
        <el-form-item label="新密碼">
          <el-input v-model="passwordForm.newPassword" type="password" show-password />
        </el-form-item>
        <el-form-item label="確認密碼">
          <el-input v-model="passwordForm.confirmPassword" type="password" show-password />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showPasswordDialog = false">取消</el-button>
        <el-button type="primary" @click="changePassword">確認變更</el-button>
      </template>
    </el-dialog>

    <!-- 更改電子郵件對話框 -->
    <el-dialog v-model="showEmailDialog" title="更改電子郵件" width="500px">
      <el-form label-width="100px">
        <el-form-item label="新電子郵件">
          <el-input v-model="emailForm.newEmail" type="email" placeholder="請輸入新的電子郵件地址" />
        </el-form-item>
        <el-form-item label="確認密碼">
          <el-input v-model="emailForm.password" type="password" placeholder="請輸入密碼以確認" show-password />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showEmailDialog = false">取消</el-button>
        <el-button type="primary" @click="confirmChangeEmail">確認更改</el-button>
      </template>
    </el-dialog>

    <!-- LINE QR Code 對話框 -->
    <el-dialog v-model="showLineQRDialog" title="LINE QR Code" width="400px" align-center>
      <div style="text-align: center;">
        <div id="lineQRCode" style="display: inline-block;"></div>
        <p style="margin-top: 20px; color: #606266;">
          掃描此 QR Code 加我為 LINE 好友
        </p>
        <p style="color: #909399; font-size: 14px;">
          LINE ID: <strong>{{ socialLinks.line }}</strong>
        </p>
      </div>
      <template #footer>
        <el-button type="primary" @click="showLineQRDialog = false">關閉</el-button>
      </template>
    </el-dialog>

  <!-- 啟用兩步驟驗證對話框 -->
  <el-dialog v-model="showTwoFactorDialog" title="啟用兩步驟驗證" width="500px" :before-close="handleTwoFactorBeforeClose">
      <div style="text-align: center;">
        <el-steps :active="twoFactorStep" finish-status="success" style="margin-bottom: 20px;">
          <el-step title="掃描 QR Code" />
          <el-step title="輸入驗證碼" />
        </el-steps>
        
        <div v-if="twoFactorStep === 0">
          <p style="margin-bottom: 20px; color: #606266;">
            請使用 Google Authenticator 或其他驗證 App 掃描此 QR Code
          </p>
          <div id="twoFactorQRCode" style="display: inline-block; margin-bottom: 20px;"></div>
          <p style="color: #909399; font-size: 14px;">
            或手動輸入密鑰：<br>
            <el-input 
              v-model="twoFactorSecret" 
              readonly 
              style="max-width: 300px; margin-top: 10px;"
            >
              <template #append>
                <el-button @click="copySecret">複製</el-button>
              </template>
            </el-input>
          </p>
        </div>
        
        <div v-if="twoFactorStep === 1">
          <p style="margin-bottom: 20px; color: #606266;">
            <!-- 請輸入驗證 App 顯示的 6 位數驗證碼 -->
          </p>
          <el-input
            v-model="twoFactorCode"
            placeholder="請輸入驗證器顯示 6 位數驗證碼"
            maxlength="60"
            style="max-width: 500px; font-size: 12px; text-align: center;"
            @keyup.enter="verifyTwoFactorCode"
          />
        </div>
      </div>
      <template #footer>
        <el-button @click="cancelTwoFactor">取消</el-button>
        <el-button v-if="twoFactorStep === 0" type="primary" @click="twoFactorStep = 1">下一步</el-button>
        <el-button v-if="twoFactorStep === 1" @click="twoFactorStep = 0">上一步</el-button>
        <el-button v-if="twoFactorStep === 1" type="primary" @click="verifyTwoFactorCode">確認</el-button>
      </template>
    </el-dialog>

  <!-- 停用兩步驟驗證對話框 -->
  <el-dialog v-model="showDisableTwoFactorDialog" title="停用兩步驟驗證" width="450px" :before-close="handleDisableTwoFactorBeforeClose">
      <el-alert
        title="警告"
        type="warning"
        :closable="false"
        style="margin-bottom: 20px;"
      >
        停用兩步驟驗證會降低您的帳號安全性
      </el-alert>
      <el-form label-width="100px">
        <el-form-item label="驗證碼">
          <el-input
            v-model="disableTwoFactorCode"
            placeholder="請輸入目前的 6 位數驗證碼"
            maxlength="6"
            @keyup.enter="confirmDisableTwoFactor"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDisableTwoFactorDialog = false">取消</el-button>
        <el-button type="danger" @click="confirmDisableTwoFactor">確認停用</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Upload,
  Select,
  InfoFilled,
  Link,
  Right,
  Connection
} from '@element-plus/icons-vue'
import NavBar from '@/components/NavBar.vue'
import axios from '@/utils/axios'

const router = useRouter()

const activeTab = ref('basic')

// 地區選擇器配置
const selectedLocation = ref([])
const cascaderProps = {
  expandTrigger: 'hover',
  value: 'value',
  label: 'label',
  children: 'children'
}

// 地區選項數據
const locationOptions = [
  {
    value: '台灣',
    label: '台灣',
    children: [
      { value: '台北市', label: '台北市' },
      { value: '新北市', label: '新北市' },
      { value: '桃園市', label: '桃園市' },
      { value: '台中市', label: '台中市' },
      { value: '台南市', label: '台南市' },
      { value: '高雄市', label: '高雄市' },
      { value: '基隆市', label: '基隆市' },
      { value: '新竹市', label: '新竹市' },
      { value: '嘉義市', label: '嘉義市' },
      { value: '新竹縣', label: '新竹縣' },
      { value: '苗栗縣', label: '苗栗縣' },
      { value: '彰化縣', label: '彰化縣' },
      { value: '南投縣', label: '南投縣' },
      { value: '雲林縣', label: '雲林縣' },
      { value: '嘉義縣', label: '嘉義縣' },
      { value: '屏東縣', label: '屏東縣' },
      { value: '宜蘭縣', label: '宜蘭縣' },
      { value: '花蓮縣', label: '花蓮縣' },
      { value: '台東縣', label: '台東縣' },
      { value: '澎湖縣', label: '澎湖縣' },
      { value: '金門縣', label: '金門縣' },
      { value: '連江縣', label: '連江縣' }
    ]
  },
  {
    value: '日本',
    label: '日本',
    children: [
      { value: '東京', label: '東京' },
      { value: '大阪', label: '大阪' },
      { value: '京都', label: '京都' },
      { value: '北海道', label: '北海道' },
      { value: '沖繩', label: '沖繩' },
      { value: '福岡', label: '福岡' },
      { value: '名古屋', label: '名古屋' },
      { value: '神戶', label: '神戶' },
      { value: '橫濱', label: '橫濱' },
      { value: '奈良', label: '奈良' }
    ]
  },
  {
    value: '韓國',
    label: '韓國',
    children: [
      { value: '首爾', label: '首爾' },
      { value: '釜山', label: '釜山' },
      { value: '濟州島', label: '濟州島' },
      { value: '仁川', label: '仁川' },
      { value: '大邱', label: '大邱' },
      { value: '光州', label: '光州' }
    ]
  },
  {
    value: '中國',
    label: '中國',
    children: [
      { value: '北京', label: '北京' },
      { value: '上海', label: '上海' },
      { value: '廣州', label: '廣州' },
      { value: '深圳', label: '深圳' },
      { value: '成都', label: '成都' },
      { value: '杭州', label: '杭州' },
      { value: '西安', label: '西安' },
      { value: '重慶', label: '重慶' },
      { value: '南京', label: '南京' },
      { value: '武漢', label: '武漢' }
    ]
  },
  {
    value: '香港',
    label: '香港',
    children: [
      { value: '香港島', label: '香港島' },
      { value: '九龍', label: '九龍' },
      { value: '新界', label: '新界' }
    ]
  },
  {
    value: '新加坡',
    label: '新加坡',
    children: [
      { value: '新加坡', label: '新加坡' }
    ]
  },
  {
    value: '泰國',
    label: '泰國',
    children: [
      { value: '曼谷', label: '曼谷' },
      { value: '清邁', label: '清邁' },
      { value: '普吉', label: '普吉' },
      { value: '芭達雅', label: '芭達雅' },
      { value: '蘇梅島', label: '蘇梅島' }
    ]
  },
  {
    value: '美國',
    label: '美國',
    children: [
      { value: '紐約', label: '紐約' },
      { value: '洛杉磯', label: '洛杉磯' },
      { value: '舊金山', label: '舊金山' },
      { value: '西雅圖', label: '西雅圖' },
      { value: '芝加哥', label: '芝加哥' },
      { value: '波士頓', label: '波士頓' },
      { value: '拉斯維加斯', label: '拉斯維加斯' },
      { value: '邁阿密', label: '邁阿密' }
    ]
  },
  {
    value: '英國',
    label: '英國',
    children: [
      { value: '倫敦', label: '倫敦' },
      { value: '曼徹斯特', label: '曼徹斯特' },
      { value: '愛丁堡', label: '愛丁堡' },
      { value: '利物浦', label: '利物浦' },
      { value: '劍橋', label: '劍橋' },
      { value: '牛津', label: '牛津' }
    ]
  },
  {
    value: '法國',
    label: '法國',
    children: [
      { value: '巴黎', label: '巴黎' },
      { value: '馬賽', label: '馬賽' },
      { value: '里昂', label: '里昂' },
      { value: '尼斯', label: '尼斯' },
      { value: '史特拉斯堡', label: '史特拉斯堡' }
    ]
  },
  {
    value: '澳洲',
    label: '澳洲',
    children: [
      { value: '雪梨', label: '雪梨' },
      { value: '墨爾本', label: '墨爾本' },
      { value: '布里斯本', label: '布里斯本' },
      { value: '伯斯', label: '伯斯' },
      { value: '阿德萊德', label: '阿德萊德' }
    ]
  },
  {
    value: '其他',
    label: '其他',
    children: [
      { value: '其他地區', label: '其他地區' }
    ]
  }
]

// 處理地區變更
const handleLocationChange = (value) => {
  if (value && value.length === 2) {
    // 組合為 "國家 - 城市" 格式
    editForm.location = `${value[0]} - ${value[1]}`
  } else {
    editForm.location = ''
  }
}

// 用戶資料
const userProfile = ref({
  name: 'Test User',
  email: 'test@example.com',
  gender: 'male',
  age: 28,
  location: '台北市',
  bio: '喜歡登山、露營，尋找志同道合的旅伴！',
  avatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
  verified: true,
  joinDate: '2025-01-01',
  stats: {
    activities: 5,
    matches: 12,
    reviews: 8
  }
})

// 編輯表單
const editForm = reactive({
  name: '',
  gender: '',
  age: 0,
  location: '',
  bio: '',
  interests: []
})

// 興趣標籤
const showInterestInput = ref(false)
const newInterest = ref('')

// 隱私設定
const privacySettings = reactive({
  profileVisibility: 'public',
  socialPrivacy: 'public',  // public 或 friends_only
  showAge: true,
  showLocation: true,
  allowStrangerMessages: true
})

// 安全設定
const securitySettings = reactive({
  twoFactorAuth: false
})

// 兩步驟驗證相關
const showTwoFactorDialog = ref(false)
const showDisableTwoFactorDialog = ref(false)
const twoFactorStep = ref(0)
const twoFactorSecret = ref('')
const twoFactorCode = ref('')
const disableTwoFactorCode = ref('')
const twoFactorLoading = ref(false)

// 社群帳號
const socialLinks = reactive({
  instagram: '',
  facebook: '',
  line: '',
  twitter: ''
})

// 保存原始社群帳號資料
const originalSocialLinks = reactive({
  instagram: '',
  facebook: '',
  line: '',
  twitter: ''
})

const showLineQRDialog = ref(false)

// 密碼變更
const showPasswordDialog = ref(false)
const passwordForm = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// 載入用戶資料
onMounted(async () => {
  try {
    // 從 API 載入用戶資料
    const response = await axios.get('/users/profile')
    
    if (response.data && response.data.user) {
      const user = response.data.user
      userProfile.value = {
        name: user.name,
        email: user.email,
        gender: user.gender || 'male',
        age: user.age || 18,
        location: user.location || '',
        bio: user.bio || '',
        avatar: user.avatar || 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
        verified: user.is_verified || false,
        joinDate: new Date(user.join_date).toLocaleDateString('zh-TW'),
        stats: {
          activities: 0,
          matches: 0,
          reviews: user.rating_count || 0
        }
      }
      
      // 初始化編輯表單
      editForm.name = userProfile.value.name
      editForm.gender = userProfile.value.gender
      editForm.age = userProfile.value.age
      editForm.location = userProfile.value.location
      editForm.bio = userProfile.value.bio
      editForm.interests = user.interests || []  // 載入興趣標籤
      
      // 載入社群帳號
      if (user.social_links) {
        socialLinks.instagram = user.social_links.instagram || ''
        socialLinks.facebook = user.social_links.facebook || ''
        socialLinks.line = user.social_links.line || ''
        socialLinks.twitter = user.social_links.twitter || ''
        
        // 保存原始資料
        originalSocialLinks.instagram = user.social_links.instagram || ''
        originalSocialLinks.facebook = user.social_links.facebook || ''
        originalSocialLinks.line = user.social_links.line || ''
        originalSocialLinks.twitter = user.social_links.twitter || ''
      }
      
      // 載入隱私設定
      if (user.privacy_setting) {
        privacySettings.profileVisibility = user.privacy_setting
      }
      if (user.social_privacy) {
        privacySettings.socialPrivacy = user.social_privacy
      }
      
      // 載入兩步驟驗證狀態
      if (user.two_factor_enabled !== undefined) {
        securitySettings.twoFactorAuth = user.two_factor_enabled
      }
      
      // 解析地區並設置級聯選擇器
      parseLocationString(userProfile.value.location)
    }
    
    // 載入統計數據
    const statsResponse = await axios.get('/users/stats')
    if (statsResponse.data && statsResponse.data.stats) {
      userProfile.value.stats.activities = statsResponse.data.stats.activities
      userProfile.value.stats.matches = statsResponse.data.stats.matches
    }
    
  } catch (error) {
    console.error('載入用戶資料失敗:', error)
    
    // 如果 API 失敗，從 localStorage 讀取
    const userStr = localStorage.getItem('user')
    if (userStr) {
      const user = JSON.parse(userStr)
      userProfile.value = { ...userProfile.value, ...user }
    }
    
    // 初始化編輯表單
    editForm.name = userProfile.value.name
    editForm.gender = userProfile.value.gender
    editForm.age = userProfile.value.age
    editForm.location = userProfile.value.location
    editForm.bio = userProfile.value.bio
    editForm.interests = userProfile.value.interests || []  // 載入興趣標籤
    
    // 解析地區並設置級聯選擇器
    parseLocationString(userProfile.value.location)
  }
})

// 解析地區字串並設置級聯選擇器
const parseLocationString = (locationStr) => {
  if (!locationStr) {
    selectedLocation.value = []
    return
  }
  
  // 如果格式是 "國家 - 城市"
  if (locationStr.includes(' - ')) {
    const parts = locationStr.split(' - ')
    selectedLocation.value = [parts[0], parts[1]]
  } else {
    // 舊格式,嘗試匹配
    // 檢查是否為台灣的縣市
    const taiwanCities = locationOptions[0].children.map(c => c.value)
    if (taiwanCities.includes(locationStr)) {
      selectedLocation.value = ['台灣', locationStr]
    } else {
      // 無法解析,清空
      selectedLocation.value = []
    }
  }
}

// 性別文字
const getGenderText = (gender) => {
  const texts = {
    male: '男性',
    female: '女性',
    other: '其他'
  }
  return texts[gender] || '未設定'
}

// 返回
const goBack = () => {
  router.back()
}

// 上傳頭像
const avatarInput = ref(null)

const uploadAvatar = () => {
  avatarInput.value?.click()
}

const handleAvatarUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  if (!file.type.startsWith('image/')) {
    ElMessage.error('請選擇圖片檔案')
    return
  }

  if (file.size > 2 * 1024 * 1024) {
    ElMessage.error('圖片大小不能超過 2MB')
    return
  }

  try {
    // 上傳到服務器
    const formData = new FormData()
    formData.append('image', file)
    
    const token = localStorage.getItem('token')
    const response = await fetch('/api/upload/image', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: formData
    })
    
    if (!response.ok) {
      throw new Error('上傳失敗')
    }
    
    const data = await response.json()
    
    // 更新頭像 URL
    editForm.avatar = data.url
    userProfile.value.avatar = data.url
    
    // 更新到後端用戶資料
    await axios.put('/users/profile', {
      profile_picture: data.url
    })
    
    // 更新本地存儲
    const user = JSON.parse(localStorage.getItem('user'))
    user.profile_picture = data.url
    user.avatar = data.url
    localStorage.setItem('user', JSON.stringify(user))
    
    ElMessage.success('頭像上傳成功！')
    
    // 重新載入用戶資料
    await loadUserProfile()
  } catch (error) {
    console.error('上傳頭像失敗:', error)
    ElMessage.error('頭像上傳失敗，請重試')
  }
  
  // 清空 input
  event.target.value = ''
}

// 新增興趣
const addInterest = () => {
  if (newInterest.value && !editForm.interests.includes(newInterest.value)) {
    editForm.interests.push(newInterest.value)
  }
  newInterest.value = ''
  showInterestInput.value = false
}

// 移除興趣
const removeInterest = (tag) => {
  editForm.interests = editForm.interests.filter(t => t !== tag)
}

// 儲存個人資料
const saveProfile = async () => {
  try {
    const response = await axios.put('/users/profile', {
      name: editForm.name,
      gender: editForm.gender,
      age: editForm.age,
      location: editForm.location,
      bio: editForm.bio,
      interests: editForm.interests  // 添加興趣標籤
    })
    
    if (response.data) {
      userProfile.value.name = editForm.name
      userProfile.value.gender = editForm.gender
      userProfile.value.age = editForm.age
      userProfile.value.location = editForm.location
      userProfile.value.bio = editForm.bio
      userProfile.value.interests = editForm.interests  // 更新興趣
      
      // 更新 localStorage
      const user = JSON.parse(localStorage.getItem('user'))
      user.name = editForm.name
      user.interests = editForm.interests  // 保存興趣到 localStorage
      localStorage.setItem('user', JSON.stringify(user))
      
      ElMessage.success('個人資料已更新')
    }
  } catch (error) {
    console.error('更新個人資料失敗:', error)
    ElMessage.error('更新失敗，請稍後再試')
  }
}

// 取消編輯
const cancelEdit = () => {
  editForm.name = userProfile.value.name
  editForm.gender = userProfile.value.gender
  editForm.age = userProfile.value.age
  editForm.location = userProfile.value.location
  editForm.bio = userProfile.value.bio
  editForm.interests = userProfile.value.interests || []  // 恢復興趣標籤
}

// 儲存社群帳號
const saveSocialLinks = async () => {
  try {
    const response = await axios.put('/users/profile', {
      social_links: {
        instagram: socialLinks.instagram,
        facebook: socialLinks.facebook,
        line: socialLinks.line,
        twitter: socialLinks.twitter
      }
    })
    
    if (response.data) {
      ElMessage.success('社群帳號已更新')
      // 更新原始資料
      originalSocialLinks.instagram = socialLinks.instagram
      originalSocialLinks.facebook = socialLinks.facebook
      originalSocialLinks.line = socialLinks.line
      originalSocialLinks.twitter = socialLinks.twitter
    }
  } catch (error) {
    console.error('更新社群帳號失敗:', error)
    ElMessage.error('更新失敗，請稍後再試')
  }
}

// 取消社群帳號編輯
const cancelSocialEdit = () => {
  socialLinks.instagram = originalSocialLinks.instagram
  socialLinks.facebook = originalSocialLinks.facebook
  socialLinks.line = originalSocialLinks.line
  socialLinks.twitter = originalSocialLinks.twitter
}

// 打開社群連結
const openSocialLink = (url) => {
  if (url) {
    // 確保 URL 包含 http:// 或 https://
    const fullUrl = url.startsWith('http') ? url : `https://${url}`
    window.open(fullUrl, '_blank')
  }
}

// 顯示 LINE QR Code
const showLineQRCode = () => {
  if (!socialLinks.line) {
    ElMessage.warning('請先輸入 LINE ID')
    return
  }
  
  showLineQRDialog.value = true
  
  // 等待對話框渲染後生成 QR Code
  setTimeout(() => {
    generateLineQRCode()
  }, 100)
}

// 生成 LINE QR Code
const generateLineQRCode = () => {
  const container = document.getElementById('lineQRCode')
  if (!container) return
  
  // 清空容器
  container.innerHTML = ''
  
  // 使用 LINE 官方的 QR Code URL
  const lineUrl = `https://line.me/ti/p/${encodeURIComponent(socialLinks.line)}`
  
  // 使用第三方 QR Code 生成服務
  const qrCodeUrl = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(lineUrl)}`
  
  const img = document.createElement('img')
  img.src = qrCodeUrl
  img.alt = 'LINE QR Code'
  img.style.maxWidth = '100%'
  
  container.appendChild(img)
}

// 儲存隱私設定
const savePrivacySettings = async () => {
  try {
    const response = await axios.put('/users/privacy', {
      privacy_setting: privacySettings.profileVisibility,
      social_privacy: privacySettings.socialPrivacy
    })
    
    if (response.data) {
      ElMessage.success('隱私設定已更新')
      console.log('已更新隱私設定:', response.data)
    }
  } catch (error) {
    console.error('更新隱私設定失敗:', error)
    ElMessage.error('更新失敗，請稍後再試')
  }
}

// 更改電子郵件
const showEmailDialog = ref(false)
const emailForm = ref({
  newEmail: '',
  password: ''
})

const changeEmail = () => {
  showEmailDialog.value = true
  emailForm.value = { newEmail: '', password: '' }
}

const confirmChangeEmail = async () => {
  if (!emailForm.value.newEmail || !emailForm.value.password) {
    ElMessage.error('請填寫所有欄位')
    return
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(emailForm.value.newEmail)) {
    ElMessage.error('請輸入有效的電子郵件地址')
    return
  }

  // TODO: 需要後端API支援
  ElMessage.info('更改電子郵件功能需要後端API支援，包括驗證碼發送和驗證流程')
  showEmailDialog.value = false
}

// 變更密碼
const changePassword = async () => {
  if (!passwordForm.currentPassword || !passwordForm.newPassword || !passwordForm.confirmPassword) {
    ElMessage.error('請填寫所有欄位')
    return
  }
  
  if (passwordForm.newPassword !== passwordForm.confirmPassword) {
    ElMessage.error('兩次輸入的密碼不一致')
    return
  }
  
  if (passwordForm.newPassword.length < 6) {
    ElMessage.error('密碼長度至少需要 6 個字元')
    return
  }
  
  try {
    await axios.post('/auth/change-password', {
      old_password: passwordForm.currentPassword,
      new_password: passwordForm.newPassword
    })
    
    ElMessage.success('密碼已變更，請重新登入')
    showPasswordDialog.value = false
    
    // 重置表單
    passwordForm.currentPassword = ''
    passwordForm.newPassword = ''
    passwordForm.confirmPassword = ''
    
    // 登出並跳轉到登入頁
    setTimeout(() => {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      router.push('/login')
    }, 1500)
    
  } catch (error) {
    console.error('變更密碼失敗:', error)
    if (error.response?.data?.error) {
      ElMessage.error(error.response.data.error)
    } else {
      ElMessage.error('變更密碼失敗')
    }
  }
}

// 處理兩步驟驗證開關變化
const handleTwoFactorChange = async (value) => {
  if (value) {
    // 啟用兩步驟驗證
    try {
      twoFactorLoading.value = true
      const response = await axios.post('/auth/2fa/setup')
      
      if (response.data && response.data.secret) {
        twoFactorSecret.value = response.data.secret
        showTwoFactorDialog.value = true
        twoFactorStep.value = 0
        twoFactorCode.value = ''
        
        // 等待對話框渲染後生成 QR Code
        setTimeout(() => {
          generateTwoFactorQRCode()
        }, 100)
      }
    } catch (error) {
      console.error('設定兩步驟驗證失敗:', error, error.response?.data)
      // 顯示後端返回的錯誤訊息（如果有），否則使用通用提示
      const msg = error.response?.data?.error || error.response?.data?.message || '設定失敗，請稍後再試'
      ElMessage.error(msg)
      securitySettings.twoFactorAuth = false
    } finally {
      twoFactorLoading.value = false
    }
  } else {
    // 停用兩步驟驗證
    disableTwoFactorCode.value = ''
    showDisableTwoFactorDialog.value = true
  }
}

// 生成兩步驟驗證 QR Code
const generateTwoFactorQRCode = () => {
  const container = document.getElementById('twoFactorQRCode')
  if (!container) return
  
  container.innerHTML = ''
  
  const user = JSON.parse(localStorage.getItem('user') || '{}')
  const email = user.email || userProfile.value.email
  const appName = 'EdgeSurvivor'
  
  // 生成 TOTP URI
  const totpUri = `otpauth://totp/${encodeURIComponent(appName)}:${encodeURIComponent(email)}?secret=${twoFactorSecret.value}&issuer=${encodeURIComponent(appName)}`
  
  // 使用第三方 QR Code 生成服務
  const qrCodeUrl = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(totpUri)}`
  
  const img = document.createElement('img')
  img.src = qrCodeUrl
  img.alt = '兩步驟驗證 QR Code'
  img.style.maxWidth = '100%'
  
  container.appendChild(img)
}

// 複製密鑰
const copySecret = () => {
  navigator.clipboard.writeText(twoFactorSecret.value)
    .then(() => {
      ElMessage.success('密鑰已複製到剪貼簿')
    })
    .catch(() => {
      ElMessage.error('複製失敗')
    })
}

// 驗證兩步驟驗證碼
const verifyTwoFactorCode = async () => {
  if (!twoFactorCode.value || twoFactorCode.value.length !== 6) {
    ElMessage.error('請輸入 6 位數驗證碼')
    return
  }
  
  try {
    const response = await axios.post('/auth/2fa/verify', {
      code: twoFactorCode.value
    })
    
    if (response.data && response.data.success) {
      ElMessage.success('兩步驟驗證已啟用')
      showTwoFactorDialog.value = false
      securitySettings.twoFactorAuth = true
    } else {
      ElMessage.error('驗證碼錯誤，請重試')
    }
  } catch (error) {
    console.error('驗證失敗:', error)
    if (error.response?.data?.error) {
      ElMessage.error(error.response.data.error)
    } else {
      ElMessage.error('驗證失敗，請重試')
    }
  }
}

// 取消兩步驟驗證設定
const cancelTwoFactor = () => {
  showTwoFactorDialog.value = false
  securitySettings.twoFactorAuth = false
}

// Dialog before-close handlers: called when user clicks the dialog X or backdrop.
// Ensure toggle state and temporary data are reverted if user dismisses dialogs.
const handleTwoFactorBeforeClose = (done) => {
  // User dismissed enable flow without verifying -> revert the switch and clear temp data
  securitySettings.twoFactorAuth = false
  twoFactorSecret.value = ''
  twoFactorCode.value = ''
  twoFactorStep.value = 0
  done()
}

const handleDisableTwoFactorBeforeClose = (done) => {
  // User dismissed disable flow -> keep 2FA enabled and clear input
  securitySettings.twoFactorAuth = true
  disableTwoFactorCode.value = ''
  done()
}

// 確認停用兩步驟驗證
const confirmDisableTwoFactor = async () => {
  if (!disableTwoFactorCode.value || disableTwoFactorCode.value.length !== 6) {
    ElMessage.error('請輸入 6 位數驗證碼')
    return
  }
  
  try {
    const response = await axios.post('/auth/2fa/disable', {
      code: disableTwoFactorCode.value
    })
    
    if (response.data && response.data.success) {
      ElMessage.success('兩步驟驗證已停用')
      showDisableTwoFactorDialog.value = false
      securitySettings.twoFactorAuth = false
    } else {
      ElMessage.error('驗證碼錯誤，請重試')
    }
  } catch (error) {
    console.error('停用失敗:', error)
    if (error.response?.data?.error) {
      ElMessage.error(error.response.data.error)
    } else {
      ElMessage.error('停用失敗，請重試')
    }
  }
}

// 刪除帳號
const deleteAccount = async () => {
  try {
    await ElMessageBox.confirm(
      '刪除帳號後將無法恢復，所有資料將被永久刪除。確定要刪除嗎？',
      '危險操作',
      {
        confirmButtonText: '確定刪除',
        cancelButtonText: '取消',
        type: 'error',
        confirmButtonClass: 'el-button--danger'
      }
    )

    // 二次確認
    const result = await ElMessageBox.prompt(
      '請輸入您的密碼以確認刪除帳號',
      '確認密碼',
      {
        confirmButtonText: '確定',
        cancelButtonText: '取消',
        inputType: 'password',
        inputPlaceholder: '請輸入密碼',
        inputValidator: (value) => {
          if (!value) {
            return '請輸入密碼'
          }
          return true
        }
      }
    )

    // 執行刪除
    await axios.delete('/users/account', {
      data: { password: result.value }
    })
    
    ElMessage.success('帳號已刪除')
    
    // 清除本地資料並跳轉
    setTimeout(() => {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      router.push('/login')
    }, 1000)
    
  } catch (error) {
    if (error === 'cancel') {
      // 用戶取消
      return
    }
    console.error('刪除帳號失敗:', error)
    if (error.response?.data?.error) {
      ElMessage.error(error.response.data.error)
    } else {
      ElMessage.error('刪除帳號失敗')
    }
  }
}
</script>

<style scoped>
.profile {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.profile-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.profile-row {
  margin-top: 20px;
}

.profile-card {
  text-align: center;
}

.avatar-section {
  margin-bottom: 20px;
}

.upload-btn {
  margin-top: 10px;
}

.user-basic-info {
  margin-bottom: 20px;
}

.user-basic-info h2 {
  margin: 10px 0;
}

.user-details {
  margin: 20px 0;
}

.profile-stats {
  display: flex;
  justify-content: space-around;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #dcdfe6;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #409eff;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 5px;
}

.social-links-display {
  display: flex;
  justify-content: center;
  gap: 15px;
  padding: 15px 0;
  flex-wrap: wrap;
}

.social-links-display .el-button {
  transition: transform 0.2s, box-shadow 0.2s;
}

.social-links-display .el-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

/* 社群帳號綁定樣式 */
.social-binding-header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 24px;
  margin: -20px -20px 24px -20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 4px 4px 0 0;
  color: white;
}

.social-binding-header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  margin: -20px -20px 24px -20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 8px 8px 0 0;
  color: white;
}

.social-binding-header h3 {
  margin: 0 0 4px 0;
  font-size: 18px;
  font-weight: 600;
}

.social-binding-header p {
  margin: 0;
  font-size: 13px;
  opacity: 0.9;
}

.social-form {
  padding: 0 4px;
}

.social-input-group {
  position: relative;
  margin-bottom: 24px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 12px;
  border: 2px solid transparent;
  transition: all 0.3s ease;
}

.social-input-group:hover {
  background: #ffffff;
  border-color: #e0e0e0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.social-label {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.social-icon {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  transition: transform 0.3s ease;
}

.social-input-group:hover .social-icon {
  transform: scale(1.1);
}

.instagram-icon {
  background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%);
}

.facebook-icon {
  background: #1877F2;
}

.line-icon {
  background: #00B900;
}

.twitter-icon {
  background: #000000;
}

.social-icon svg {
  width: 20px;
  height: 20px;
  color: white;
}

.social-label span {
  font-size: 15px;
  font-weight: 600;
  color: #303133;
}

.social-input-group .el-input {
  flex: 1;
}

.visit-btn {
  position: absolute;
  right: 20px;
  top: 68px;
  background: #409eff;
  color: white;
  border: none;
  transition: all 0.3s ease;
}

.visit-btn:hover {
  background: #337ecc;
  transform: scale(1.1);
}

.input-hint {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 8px;
  padding: 8px 12px;
  background: #e8f4fd;
  border-radius: 6px;
  font-size: 12px;
  color: #606266;
}

.input-hint .el-icon {
  color: #409eff;
}

.form-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #e4e7ed;
}

.form-actions .el-button {
  min-width: 120px;
}

@media (max-width: 768px) {
  .profile-container {
    padding: 10px;
  }
  
  .social-binding-header {
    flex-direction: column;
    text-align: center;
  }
  
  .social-input-group {
    padding: 16px;
  }
  
  .visit-btn {
    position: static;
    margin-top: 12px;
    width: 100%;
  }
}
</style>
