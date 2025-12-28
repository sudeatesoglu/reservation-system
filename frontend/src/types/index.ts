// User types
export interface User {
  id: number;
  email: string;
  username: string;
  full_name: string;
  phone?: string;
  role: 'admin' | 'student' | 'staff';
  is_active: boolean;
  created_at: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
  full_name: string;
  role: 'student' | 'staff';
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

// Resource types
export interface Resource {
  id: string;
  name: string;
  resource_type: 'meeting_room' | 'study_room' | 'computer_lab' | 'office' | 'library_desk';
  description?: string;
  capacity: number;
  location: string;
  building?: string;
  floor?: number;
  amenities: string[];
  available_days: number[];
  available_hours: {
    start_time: string;
    end_time: string;
  };
  slot_duration_minutes: number;
  max_booking_hours: number;
  requires_approval: boolean;
  status: 'available' | 'maintenance' | 'unavailable';
  created_at: string;
  updated_at?: string | null;
}

export interface ResourceCreate {
  name: string;
  resource_type: 'meeting_room' | 'study_room' | 'computer_lab' | 'office' | 'library_desk';
  description?: string;
  location: string;
  building?: string;
  floor?: number;
  capacity?: number;
  amenities?: string[];
  available_days?: number[];
  available_hours?: {
    start_time: string;
    end_time: string;
  };
  slot_duration_minutes?: number;
  max_booking_hours?: number;
  requires_approval?: boolean;
}

// Reservation types
export interface Reservation {
  id: string;
  user_id: number;
  username: string;
  resource_id: string;
  resource_name?: string;
  date: string;
  start_time: string;
  end_time: string;
  purpose?: string;
  notes?: string;
  status: 'pending' | 'confirmed' | 'cancelled' | 'completed' | 'no_show';
  created_at: string;
  updated_at?: string | null;
  cancelled_at?: string | null;
  cancellation_reason?: string | null;
}

export interface ReservationCreate {
  resource_id: string;
  date: string;
  start_time: string;
  end_time: string;
  purpose?: string;
  notes?: string;
}

// API Response types
export interface ApiError {
  detail: string;
}
