import type { Reservation } from '../types';

interface ReservationListProps {
  reservations: Reservation[];
  onCancel: (id: string) => void;
}

export default function ReservationList({ reservations, onCancel }: ReservationListProps) {
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      weekday: 'short',
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  const formatTime = (timeString: string) => {
    // timeString is in format "HH:MM"
    const [hours, minutes] = timeString.split(':');
    const date = new Date();
    date.setHours(parseInt(hours), parseInt(minutes));
    return date.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'confirmed':
        return 'status-confirmed';
      case 'pending':
        return 'status-pending';
      case 'cancelled':
        return 'status-cancelled';
      case 'completed':
        return 'status-completed';
      default:
        return '';
    }
  };

  if (reservations.length === 0) {
    return (
      <div className="empty-message">
        <p>You don't have any reservations yet.</p>
        <p>Go to "Available Resources" to make your first booking!</p>
      </div>
    );
  }

  return (
    <div className="reservation-list">
      {reservations.map((reservation) => (
        <div key={reservation.id} className="reservation-item">
          <div className="reservation-header">
            <span className={`status-badge ${getStatusColor(reservation.status)}`}>
              {reservation.status}
            </span>
            <span className="reservation-id">#{reservation.id.slice(0, 8)}</span>
          </div>
          
          <div className="reservation-details">
            <div className="reservation-info">
              {reservation.resource_name && (
                <h4 className="resource-name">{reservation.resource_name}</h4>
              )}
              <div className="reservation-datetime">
                <span className="date">{formatDate(reservation.date)}</span>
                <span className="time">
                  {formatTime(reservation.start_time)} - {formatTime(reservation.end_time)}
                </span>
              </div>
            </div>
            
            {reservation.notes && (
              <p className="reservation-notes">{reservation.notes}</p>
            )}
          </div>

          <div className="reservation-actions">
            {reservation.status !== 'cancelled' && reservation.status !== 'completed' && (
              <button
                className="btn btn-danger"
                onClick={() => onCancel(reservation.id)}
              >
                Cancel
              </button>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
