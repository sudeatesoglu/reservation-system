import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { userService } from '../services/userService';
import type { User } from '../types';
import toast from 'react-hot-toast';

export default function Profile() {
  const { user: currentUser, setUser } = useAuth();
  const [user, setUserData] = useState<User | null>(currentUser);
  const [isEditingProfile, setIsEditingProfile] = useState(false);
  const [isChangingPassword, setIsChangingPassword] = useState(false);
  
  // Profile form
  const [fullName, setFullName] = useState(currentUser?.full_name || '');
  const [email, setEmail] = useState(currentUser?.email || '');
  const [phone, setPhone] = useState(currentUser?.phone || '');
  
  // Password form
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (currentUser) {
      setUserData(currentUser);
      setFullName(currentUser.full_name || '');
      setEmail(currentUser.email || '');
      setPhone(currentUser.phone || '');
    }
  }, [currentUser]);

  const handleUpdateProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const updatedUser = await userService.updateProfile({
        full_name: fullName,
        email: email,
        phone: phone || undefined,
      });
      
      setUserData(updatedUser);
      setUser(updatedUser);
      setIsEditingProfile(false);
      toast.success('Profile updated successfully!');
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to update profile';
      toast.error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (newPassword !== confirmPassword) {
      toast.error('New passwords do not match');
      return;
    }
    
    if (newPassword.length < 8) {
      toast.error('Password must be at least 8 characters');
      return;
    }
    
    setLoading(true);
    
    try {
      await userService.changePassword({
        current_password: currentPassword,
        new_password: newPassword,
      });
      
      setCurrentPassword('');
      setNewPassword('');
      setConfirmPassword('');
      setIsChangingPassword(false);
      toast.success('Password changed successfully!');
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to change password';
      toast.error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  if (!user) {
    return <div className="loading">Loading profile...</div>;
  }

  return (
    <div className="profile-page">
      <div className="profile-container">
        <h1>👤 My Profile</h1>

        <div className="profile-card">
          <div className="profile-header">
            <div className="profile-avatar">
              {user.full_name?.charAt(0).toUpperCase() || user.username.charAt(0).toUpperCase()}
            </div>
            <div className="profile-info">
              <h2>{user.full_name || user.username}</h2>
              <p className="username">@{user.username}</p>
              <span className={`role-badge role-${user.role}`}>{user.role}</span>
            </div>
          </div>

          <div className="profile-details">
            <div className="detail-item">
              <span className="detail-label">Email:</span>
              <span className="detail-value">{user.email}</span>
            </div>
            {user.phone && (
              <div className="detail-item">
                <span className="detail-label">Phone:</span>
                <span className="detail-value">{user.phone}</span>
              </div>
            )}
            <div className="detail-item">
              <span className="detail-label">Member Since:</span>
              <span className="detail-value">
                {new Date(user.created_at).toLocaleDateString('en-US', {
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric',
                })}
              </span>
            </div>
            <div className="detail-item">
              <span className="detail-label">Account Status:</span>
              <span className={`status-badge ${user.is_active ? 'status-active' : 'status-inactive'}`}>
                {user.is_active ? 'Active' : 'Inactive'}
              </span>
            </div>
          </div>

          <div className="profile-actions">
            <button
              onClick={() => setIsEditingProfile(!isEditingProfile)}
              className="btn btn-primary"
            >
              {isEditingProfile ? '✕ Cancel Edit' : '✏️ Edit Profile'}
            </button>
            <button
              onClick={() => setIsChangingPassword(!isChangingPassword)}
              className="btn btn-secondary"
            >
              {isChangingPassword ? '✕ Cancel' : '🔒 Change Password'}
            </button>
          </div>
        </div>

        {isEditingProfile && (
          <div className="profile-card">
            <h3>Edit Profile</h3>
            <form onSubmit={handleUpdateProfile} className="profile-form">
              <div className="form-group">
                <label htmlFor="fullName">Full Name</label>
                <input
                  type="text"
                  id="fullName"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  placeholder="Enter your full name"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="email">Email</label>
                <input
                  type="email"
                  id="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="Enter your email"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="phone">Phone (Optional)</label>
                <input
                  type="tel"
                  id="phone"
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                  placeholder="Enter your phone number"
                />
              </div>

              <div className="form-actions">
                <button type="submit" className="btn btn-primary" disabled={loading}>
                  {loading ? 'Saving...' : '💾 Save Changes'}
                </button>
              </div>
            </form>
          </div>
        )}

        {isChangingPassword && (
          <div className="profile-card">
            <h3>Change Password</h3>
            <form onSubmit={handleChangePassword} className="profile-form">
              <div className="form-group">
                <label htmlFor="currentPassword">Current Password</label>
                <input
                  type="password"
                  id="currentPassword"
                  value={currentPassword}
                  onChange={(e) => setCurrentPassword(e.target.value)}
                  placeholder="Enter current password"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="newPassword">New Password</label>
                <input
                  type="password"
                  id="newPassword"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  placeholder="Enter new password (min 8 characters)"
                  required
                  minLength={8}
                />
              </div>

              <div className="form-group">
                <label htmlFor="confirmPassword">Confirm New Password</label>
                <input
                  type="password"
                  id="confirmPassword"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  placeholder="Confirm new password"
                  required
                  minLength={8}
                />
              </div>

              <div className="form-actions">
                <button type="submit" className="btn btn-primary" disabled={loading}>
                  {loading ? 'Changing...' : '🔒 Change Password'}
                </button>
              </div>
            </form>
          </div>
        )}
      </div>
    </div>
  );
}
