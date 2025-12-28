import api from './api';
import type { User } from '../types';

export interface UpdateProfileData {
  full_name?: string;
  email?: string;
  phone?: string;
}

export interface ChangePasswordData {
  current_password: string;
  new_password: string;
}

export const userService = {
  async updateProfile(data: UpdateProfileData): Promise<User> {
    const response = await api.put<User>('/users/me', data);
    return response.data;
  },

  async changePassword(data: ChangePasswordData): Promise<{ message: string }> {
    const response = await api.post<{ message: string }>('/users/me/change-password', data);
    return response.data;
  },

  async getProfile(): Promise<User> {
    const response = await api.get<User>('/users/me');
    return response.data;
  },
};
