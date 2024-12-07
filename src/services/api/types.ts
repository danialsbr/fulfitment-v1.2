export interface ApiResponse<T = any> {
  success: boolean;
  data: T;
  message: string;
}

export interface Order {
  id: string;
  status: string;
  // Add other order fields as needed
}

export interface SystemStatus {
  success: boolean;
  message: string;
  status: 'operational' | 'maintenance' | 'error';
}