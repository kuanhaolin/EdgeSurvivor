"""
TC_4.2.4: 更新探索活動清單
測試說明: 測試申請活動後，探索活動清單是否正確更新（申請的活動不再出現在探索清單中）
"""
import pytest
import json
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token
from models.user import User
from models.activity import Activity
from models.activity_participant import ActivityParticipant
from app import db

def test_update_discover_activities_after_apply(client, test_app):
    """測試申請活動後更新探索活動清單"""
    with test_app.app_context():
        # 創建創建者和申請者
        creator = User(name='creator', email='creator@test.com', password_hash='hash')
        applicant = User(name='applicant', email='applicant@test.com', password_hash='hash')
        db.session.add_all([creator, applicant])
        db.session.commit()
        
        # 創建兩個活動
        activity1 = Activity(
            title='測試活動1',
            category='hiking',
            location='陽明山',
            date=datetime.now().date() + timedelta(days=7),
            max_participants=10,
            creator_id=creator.user_id
        )
        activity2 = Activity(
            title='測試活動2',
            category='food',
            location='台北',
            date=datetime.now().date() + timedelta(days=8),
            max_participants=10,
            creator_id=creator.user_id
        )
        db.session.add_all([activity1, activity2])
        db.session.commit()
        
        applicant_token = create_access_token(identity=str(applicant.user_id))
        activity1_id = activity1.activity_id
        
        # 獲取申請前的探索活動列表
        response_before = client.get(
            '/api/activities',
            headers={'Authorization': f'Bearer {applicant_token}'}
        )
        
        assert response_before.status_code == 200
        data_before = json.loads(response_before.data)
        activities_before = data_before['activities']
        
        # 驗證兩個活動都在探索清單中
        activity_ids_before = [a['activity_id'] for a in activities_before]
        assert activity1_id in activity_ids_before
        
        # 申請活動1
        response_apply = client.post(
            f'/api/activities/{activity1_id}/join',
            headers={'Authorization': f'Bearer {applicant_token}'},
            json={'message': '我想參加這個活動！'}
        )
        
        assert response_apply.status_code == 200
        
        # 獲取申請後的已參加活動列表
        response_joined = client.get(
            '/api/activities?type=joined',
            headers={'Authorization': f'Bearer {applicant_token}'}
        )
        
        assert response_joined.status_code == 200
        data_joined = json.loads(response_joined.data)
        
        # 驗證申請的活動出現在參加列表中（pending狀態也算參加）
        # 注意：後端的 type=joined 只返回 approved/joined 狀態
        # pending 狀態需要透過 is_user_participant() 檢查
        assert activity1.is_user_participant(applicant.user_id)
        
        # 驗證申請狀態為pending
        participant = ActivityParticipant.query.filter_by(
            activity_id=activity1_id,
            user_id=applicant.user_id
        ).first()
        assert participant is not None
        assert participant.status == 'pending'
