import { ordersApi } from './orders';
import { uploadApi } from './upload';
import { systemApi } from './system';
import { transferApi } from './transfer';

export const fulfillmentApi = {
  orders: ordersApi,
  upload: uploadApi,
  system: systemApi,
  transfer: transferApi,
};

export type { ApiResponse, Order, SystemStatus } from './types';