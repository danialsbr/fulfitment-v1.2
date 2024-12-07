from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from datetime import datetime
from khayyam import JalaliDatetime
import os
import time

app = Flask(__name__)
CORS(app)

# In-memory database
orders_db = {}

@app.route('/api/system/status', methods=['GET'])
def get_system_status():
    """Get system status."""
    return jsonify({
        'success': True,
        'data': {
            'status': 'operational',
            'message': 'System is running normally',
            'timestamp': JalaliDatetime.now().strftime("%Y/%m/%d %H:%M:%S"),
            'version': '1.0.0'
        }
    })

@app.route('/api/ping', methods=['GET'])
def ping():
    """Simple ping endpoint for latency checks."""
    return jsonify({
        'success': True,
        'data': {
            'timestamp': int(time.time() * 1000)
        },
        'message': 'pong'
    })

@app.route('/api/orders/<order_id>/transfer', methods=['PUT'])
def update_transfer_status(order_id):
    """Update transfer status for an order."""
    if order_id not in orders_db:
        return jsonify({
            'success': False,
            'message': 'Order not found'
        }), 404
        
    data = request.json
    transfer_type = data.get('transferType')
    
    if not transfer_type:
        return jsonify({
            'success': False,
            'message': 'Missing transfer type'
        }), 400
        
    orders_db[order_id]['TransferType'] = transfer_type
    orders_db[order_id]['TransferTimestamp'] = JalaliDatetime.now().strftime("%Y/%m/%d %H:%M")
    
    return jsonify({
        'success': True,
        'message': 'Transfer status updated successfully'
    })

@app.route('/api/orders', methods=['GET'])
def get_orders():
    """Get all orders."""
    orders_list = []
    for order_id, order_data in orders_db.items():
        for sku, details in order_data['SKUs'].items():
            orders_list.append({
                'id': order_id,
                'sku': sku,
                'title': details['Title'],
                'color': details['Color'],
                'quantity': details['Quantity'],
                'scanned': details['Scanned'],
                'status': 'Fulfilled' if details['Scanned'] >= details['Quantity'] else 'Pending',
                'price': details['Price'],
                'scanTimestamp': details.get('ScanTimestamp'),
                'transferType': order_data.get('TransferType'),
                'transferTimestamp': order_data.get('TransferTimestamp')
            })
    return jsonify({
        'success': True,
        'data': orders_list,
        'message': 'Orders retrieved successfully'
    })

@app.route('/api/scan', methods=['POST'])
def scan_order():
    """Scan an order."""
    data = request.json
    order_id = data.get('orderId')
    sku = data.get('sku')
    
    if not order_id or not sku:
        return jsonify({
            'success': False,
            'message': 'Missing required fields'
        }), 400
        
    if order_id not in orders_db or sku not in orders_db[order_id]['SKUs']:
        return jsonify({
            'success': False,
            'message': 'Order or SKU not found'
        }), 404
        
    # Update scanned count
    orders_db[order_id]['SKUs'][sku]['Scanned'] += 1
    
    # Update scan timestamp
    current_time = JalaliDatetime.now()
    orders_db[order_id]['SKUs'][sku]['ScanTimestamp'] = current_time.strftime("%Y/%m/%d %H:%M")
    
    return jsonify({
        'success': True,
        'message': 'Scan successful'
    })

@app.route('/api/orders/<order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    """Update order status."""
    if order_id not in orders_db:
        return jsonify({
            'success': False,
            'message': 'Order not found'
        }), 404
        
    data = request.json
    new_status = data.get('status')
    
    if not new_status:
        return jsonify({
            'success': False,
            'message': 'Missing status'
        }), 400
        
    orders_db[order_id]['Status'] = new_status
    return jsonify({
        'success': True,
        'message': 'Status updated successfully'
    })

@app.route('/api/orders/<order_id>', methods=['GET'])
def get_order_details(order_id):
    """Get details for a specific order."""
    if order_id not in orders_db:
        return jsonify({
            'success': False,
            'message': 'Order not found'
        }), 404
    
    return jsonify({
        'success': True,
        'data': orders_db[order_id],
        'message': 'Order details retrieved successfully'
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)