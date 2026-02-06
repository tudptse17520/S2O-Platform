"""
Realtime Service for S2O Platform
Infrastructure layer service for real-time communication (WebSocket/SocketIO)
No business logic - pure event emission abstraction
"""
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class RealtimeService:
    """
    Infrastructure service for real-time communication.
    Provides abstraction over WebSocket/SocketIO implementation.
    
    Usage:
        from infrastructure.services import get_realtime_service
        realtime = get_realtime_service()
        realtime.emit('order:created', data, room='branch:123')
    """
    
    def __init__(self, app=None):
        self._socketio = None
        self._available = False
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize SocketIO with Flask app"""
        try:
            from flask_socketio import SocketIO
            
            self._socketio = SocketIO(
                app,
                cors_allowed_origins="*",
                async_mode='threading',  # simpler than eventlet for students
                logger=False,
                engineio_logger=False
            )
            
            self._register_handlers()
            self._available = True
            logger.info("RealtimeService: SocketIO initialized")
            
        except ImportError:
            logger.warning("RealtimeService: Flask-SocketIO not installed")
            self._available = False
        except Exception as e:
            logger.warning(f"RealtimeService: Initialization failed - {e}")
            self._available = False
    
    def _register_handlers(self):
        """Register basic WebSocket event handlers"""
        from flask_socketio import emit, join_room, leave_room
        
        @self._socketio.on('connect')
        def handle_connect():
            emit('connected', {'status': 'connected'})
        
        @self._socketio.on('disconnect')
        def handle_disconnect():
            pass
        
        @self._socketio.on('join')
        def handle_join(data):
            room = data.get('room')
            if room:
                join_room(room)
                emit('joined', {'room': room})
        
        @self._socketio.on('leave')
        def handle_leave(data):
            room = data.get('room')
            if room:
                leave_room(room)
                emit('left', {'room': room})
    
    @property
    def is_available(self) -> bool:
        """Check if realtime service is available"""
        return self._available
    
    @property
    def socketio(self):
        """Get raw SocketIO instance (for running with socketio.run())"""
        return self._socketio
    
    def emit(self, event: str, data: Dict[str, Any], room: str = None):
        """
        Emit event to clients
        
        Args:
            event: Event name (e.g., 'order:created')
            data: Event payload
            room: Target room (optional)
        """
        if self._socketio:
            if room:
                self._socketio.emit(event, data, room=room)
            else:
                self._socketio.emit(event, data)
    
    def emit_to_rooms(self, event: str, data: Dict[str, Any], rooms: List[str]):
        """Emit event to multiple rooms"""
        for room in rooms:
            self.emit(event, data, room=room)
    
    # Room naming helpers
    @staticmethod
    def tenant_room(tenant_id: str) -> str:
        return f"tenant:{tenant_id}"
    
    @staticmethod
    def branch_room(branch_id: str) -> str:
        return f"branch:{branch_id}"
    
    @staticmethod
    def table_room(table_id: str) -> str:
        return f"table:{table_id}"


class RealtimeEvents:
    """Event name constants"""
    # Order events
    ORDER_CREATED = 'order:created'
    ORDER_STATUS_CHANGED = 'order:status_changed'
    
    # Kitchen workflow
    ITEM_COOKING = 'item:cooking'
    ITEM_READY = 'item:ready'
    ITEM_SERVED = 'item:served'
    
    # Notifications
    NOTIFICATION = 'notification'


# Global instance
realtime_service = RealtimeService()


def init_realtime_service(app):
    """Initialize global realtime service"""
    realtime_service.init_app(app)
    return realtime_service


def get_realtime_service() -> RealtimeService:
    """Get global realtime service instance"""
    return realtime_service
