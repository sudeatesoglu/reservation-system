import { reservationApi } from './api';
import type { Reservation, ReservationCreate } from '../types';

const extractArray = <T>(data: unknown): T[] => {
  if (Array.isArray(data)) return data;
  if (data && typeof data === 'object') {
    const obj = data as Record<string, unknown>;
    if (Array.isArray(obj.items)) return obj.items as T[];
    if (Array.isArray(obj.reservations)) return obj.reservations as T[];
    if (Array.isArray(obj.data)) return obj.data as T[];
  }
  return [];
};

export const reservationService = {
  async getAll(): Promise<Reservation[]> {
    const response = await reservationApi.get('/reservations');
    return extractArray<Reservation>(response.data);
  },

  async getMyReservations(): Promise<Reservation[]> {
    const response = await reservationApi.get('/reservations/my');
    return extractArray<Reservation>(response.data);
  },

  async getById(id: string): Promise<Reservation> {
    const response = await reservationApi.get<Reservation>(`/reservations/${id}`);
    return response.data;
  },

  async create(data: ReservationCreate): Promise<Reservation> {
    const response = await reservationApi.post<Reservation>('/reservations/', data);
    return response.data;
  },

  async cancel(id: string): Promise<Reservation> {
    const response = await reservationApi.post<Reservation>(`/reservations/${id}/cancel`);
    return response.data;
  },

  async getByResource(resourceId: string): Promise<Reservation[]> {
    const response = await reservationApi.get<Reservation[]>(
      `/reservations/resource/${resourceId}`
    );
    return response.data;
  },
};
