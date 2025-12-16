import pytest
import json
from datetime import date, timedelta, datetime
from models import db
from models.user import User
from models.activity import Activity
from models.expense import Expense
from models.activity_participant import ActivityParticipant


class TestUserExpenseStats:
    
    def test_get_user_stats_success(self, client, test_app):
        user1 = User(email='user1@test.com', name='User1')
        user1.set_password('password123')
        user2 = User(email='user2@test.com', name='User2')
        user2.set_password('password123')
        db.session.add_all([user1, user2])
        db.session.commit()
        
        activity = Activity(
            title='Test Activity',
            description='Test',
            date=date.today(),
            location='Taipei',
            creator_id=user1.user_id,
            status='active'
        )
        db.session.add(activity)
        db.session.commit()
        
        p1 = ActivityParticipant(
            activity_id=activity.activity_id,
            user_id=user1.user_id,
            status='approved',
            role='creator'
        )
        p2 = ActivityParticipant(
            activity_id=activity.activity_id,
            user_id=user2.user_id,
            status='approved',
            role='participant'
        )
        db.session.add_all([p1, p2])
        db.session.commit()
        
        expense1 = Expense(
            activity_id=activity.activity_id,
            payer_id=user1.user_id,
            amount=1000.00,
            description='Lunch',
            category='food',
            split_type='all',
            split_participants=json.dumps([user1.user_id, user2.user_id]),
            expense_date=date.today()
        )
        
        expense2 = Expense(
            activity_id=activity.activity_id,
            payer_id=user2.user_id,
            amount=500.00,
            description='Transport',
            category='transport',
            split_type='all',
            split_participants=json.dumps([user1.user_id, user2.user_id]),
            expense_date=date.today()
        )
        
        db.session.add_all([expense1, expense2])
        db.session.commit()
        
        login_response = client.post('/api/auth/login', json={
            'email': 'user1@test.com',
            'password': 'password123'
        })
        token = login_response.get_json()['access_token']
        
        response = client.get(
            f'/api/expenses/user/{user1.user_id}/stats',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['total_paid'] == 1000.00
        assert data['total_owed'] == 750.00
        assert data['net_balance'] == 250.00
        assert data['expense_count'] == 2
        assert data['activities_count'] == 1
    
    def test_get_user_stats_unauthorized(self, client, test_app):
        user1 = User(email='user1@test.com', name='User1')
        user1.set_password('password123')
        user2 = User(email='user2@test.com', name='User2')
        user2.set_password('password123')
        db.session.add_all([user1, user2])
        db.session.commit()
        
        login_response = client.post('/api/auth/login', json={
            'email': 'user1@test.com',
            'password': 'password123'
        })
        token = login_response.get_json()['access_token']
        
        response = client.get(
            f'/api/expenses/user/{user2.user_id}/stats',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 403
    
    def test_get_user_stats_no_auth(self, client, test_app):
        response = client.get('/api/expenses/user/1/stats')
        assert response.status_code == 401
    
    def test_get_user_stats_empty_data(self, client, test_app):
        '''Test: Handle empty data (user has no expenses)'''
        user1 = User(email='empty@test.com', name='Empty')
        user1.set_password('password123')
        db.session.add(user1)
        db.session.commit()
        
        login_response = client.post('/api/auth/login', json={
            'email': 'empty@test.com',
            'password': 'password123'
        })
        token = login_response.get_json()['access_token']
        
        response = client.get(
            f'/api/expenses/user/{user1.user_id}/stats',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['total_paid'] == 0.00
        assert data['total_owed'] == 0.00
        assert data['net_balance'] == 0.00
        assert data['expense_count'] == 0
        assert data['activities_count'] == 0
    
    def test_get_user_stats_with_date_filter(self, client, test_app):
        '''Test: Date range filtering with start_date and end_date'''
        user1 = User(email='date1@test.com', name='Date1')
        user1.set_password('password123')
        user2 = User(email='date2@test.com', name='Date2')
        user2.set_password('password123')
        db.session.add_all([user1, user2])
        db.session.commit()
        
        activity = Activity(title='Date Filter Activity', description='Test activity', date=datetime(2024, 1, 15).date(), creator_id=user1.user_id, status='completed', location='Test Location')
        db.session.add(activity)
        db.session.commit()
        
        ap1 = ActivityParticipant(activity_id=activity.activity_id, user_id=user1.user_id, status='joined')
        ap2 = ActivityParticipant(activity_id=activity.activity_id, user_id=user2.user_id, status='joined')
        db.session.add_all([ap1, ap2])
        db.session.commit()
        
        # Expense within date range
        expense1 = Expense(
            activity_id=activity.activity_id, 
            payer_id=user1.user_id, 
            amount=100, 
            description='In Range', 
            expense_date=datetime(2024, 1, 20).date(), 
            split_type='all',
            split_participants=json.dumps([user1.user_id, user2.user_id])
        )
        # Expense outside date range
        expense2 = Expense(
            activity_id=activity.activity_id, 
            payer_id=user1.user_id, 
            amount=200, 
            description='Out Range', 
            expense_date=datetime(2024, 2, 20).date(), 
            split_type='all',
            split_participants=json.dumps([user1.user_id, user2.user_id])
        )
        db.session.add_all([expense1, expense2])
        db.session.commit()
        
        login_response = client.post('/api/auth/login', json={'email': 'date1@test.com', 'password': 'password123'})
        token = login_response.get_json()['access_token']
        
        response = client.get(
            f'/api/expenses/user/{user1.user_id}/stats?start_date=2024-01-01&end_date=2024-01-31',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['total_paid'] == 100.00
        assert data['expense_count'] == 1
    
    def test_get_user_stats_invalid_date_format(self, client, test_app):
        '''Test: Invalid date format returns 400 error'''
        user1 = User(email='invalid@test.com', name='Invalid')
        user1.set_password('password123')
        db.session.add(user1)
        db.session.commit()
        
        login_response = client.post('/api/auth/login', json={'email': 'invalid@test.com', 'password': 'password123'})
        token = login_response.get_json()['access_token']
        
        response = client.get(
            f'/api/expenses/user/{user1.user_id}/stats?start_date=invalid-date',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_get_user_stats_with_activity_grouping(self, client, test_app):
        '''Test: Group by activity returns per-activity breakdown'''
        user1 = User(email='group1@test.com', name='Group1')
        user1.set_password('password123')
        user2 = User(email='group2@test.com', name='Group2')
        user2.set_password('password123')
        db.session.add_all([user1, user2])
        db.session.commit()
        
        act1 = Activity(title='Activity 1', description='Test 1', date=datetime(2024, 1, 15).date(), creator_id=user1.user_id, status='completed', location='Test Location 1')
        act2 = Activity(title='Activity 2', description='Test 2', date=datetime(2024, 1, 20).date(), creator_id=user1.user_id, status='completed', location='Test Location 2')
        db.session.add_all([act1, act2])
        db.session.commit()
        
        ap1 = ActivityParticipant(activity_id=act1.activity_id, user_id=user1.user_id, status='joined')
        ap2 = ActivityParticipant(activity_id=act1.activity_id, user_id=user2.user_id, status='joined')
        ap3 = ActivityParticipant(activity_id=act2.activity_id, user_id=user1.user_id, status='joined')
        ap4 = ActivityParticipant(activity_id=act2.activity_id, user_id=user2.user_id, status='joined')
        db.session.add_all([ap1, ap2, ap3, ap4])
        db.session.commit()
        
        expense1 = Expense(
            activity_id=act1.activity_id, 
            payer_id=user1.user_id, 
            amount=100, 
            description='Expense 1', 
            split_type='all',
            split_participants=json.dumps([user1.user_id, user2.user_id])
        )
        expense2 = Expense(
            activity_id=act2.activity_id, 
            payer_id=user1.user_id, 
            amount=200, 
            description='Expense 2', 
            split_type='all',
            split_participants=json.dumps([user1.user_id, user2.user_id])
        )
        db.session.add_all([expense1, expense2])
        db.session.commit()
        
        login_response = client.post('/api/auth/login', json={'email': 'group1@test.com', 'password': 'password123'})
        token = login_response.get_json()['access_token']
        
        response = client.get(
            f'/api/expenses/user/{user1.user_id}/stats?group_by=activity',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'by_activity' in data
        assert len(data['by_activity']) == 2
        assert 'overall' in data
        assert data['overall']['total_paid'] == 300.00
