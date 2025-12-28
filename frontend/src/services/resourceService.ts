import { resourceApi } from './api';
import type { Resource, ResourceCreate } from '../types';

export const resourceService = {
  async getAll(): Promise<Resource[]> {
    const response = await resourceApi.get('/resources');
    const data = response.data;
    // Handle different response formats
    if (Array.isArray(data)) return data;
    if (data?.items && Array.isArray(data.items)) return data.items;
    if (data?.resources && Array.isArray(data.resources)) return data.resources;
    if (data?.data && Array.isArray(data.data)) return data.data;
    return [];
  },

  async getById(id: string): Promise<Resource> {
    const response = await resourceApi.get<Resource>(`/resources/${id}`);
    return response.data;
  },

  async create(data: ResourceCreate): Promise<Resource> {
    const response = await resourceApi.post<Resource>('/resources/', data);
    return response.data;
  },

  async update(id: string, data: Partial<ResourceCreate>): Promise<Resource> {
    const response = await resourceApi.put<Resource>(`/resources/${id}`, data);
    return response.data;
  },

  async delete(id: string): Promise<void> {
    await resourceApi.delete(`/resources/${id}`);
  },

  async checkAvailability(id: string, startTime: string, endTime: string): Promise<boolean> {
    const response = await resourceApi.get<{ available: boolean }>(
      `/resources/${id}/availability`,
      { params: { start_time: startTime, end_time: endTime } }
    );
    return response.data.available;
  },

  async search(query: string): Promise<Resource[]> {
    const response = await resourceApi.get('/resources/search', {
      params: { q: query }
    });
    const data = response.data;
    if (Array.isArray(data)) return data;
    if (data?.resources && Array.isArray(data.resources)) return data.resources;
    return [];
  },

  async getFiltered(params: {
    resource_type?: string;
    building?: string;
    status?: string;
  }): Promise<Resource[]> {
    const response = await resourceApi.get('/resources', { params });
    const data = response.data;
    if (Array.isArray(data)) return data;
    if (data?.resources && Array.isArray(data.resources)) return data.resources;
    return [];
  },
};
