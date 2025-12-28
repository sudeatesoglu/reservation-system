import { useState } from 'react';
import type { FormEvent } from 'react';
import toast from 'react-hot-toast';
import type { Resource } from '../types';
import { reservationService } from '../services/reservationService';

interface BookingModalProps {
  resource: Resource;
  onClose: () => void;
  onComplete: () => void;
}

export default function BookingModal({ resource, onClose, onComplete }: BookingModalProps) {
  const [date, setDate] = useState('');
  const [startTime, setStartTime] = useState('');
  const [endTime, setEndTime] = useState('');
  const [notes, setNotes] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const startDateTime = new Date(`${date}T${startTime}`);
      const endDateTime = new Date(`${date}T${endTime}`);

      if (endDateTime <= startDateTime) {
        setError('End time must be after start time');
        setLoading(false);
        return;
      }

      await reservationService.create({
        resource_id: resource.id,
        date: date,
        start_time: startTime,
        end_time: endTime,
        notes: notes || undefined,
      });

      toast.success(`Successfully booked ${resource.name}!`, {
        icon: '✅',
      });
      onComplete();
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to create reservation. Please try again.';
      setError(errorMessage);
      toast.error(errorMessage, {
        icon: '❌',
      });
    } finally {
      setLoading(false);
    }
  };

  // Get minimum date (today)
  const today = new Date().toISOString().split('T')[0];

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Book {resource.name}</h2>
          <button className="close-btn" onClick={onClose}>×</button>
        </div>

        <div className="resource-summary">
          <p><strong>Type:</strong> {resource.resource_type.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')}</p>
          {resource.location && <p><strong>Location:</strong> {resource.location}</p>}
          <p><strong>Capacity:</strong> {resource.capacity} people</p>
        </div>

        {error && <div className="error-message">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="date">Date</label>
            <input
              type="date"
              id="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
              min={today}
              required
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="startTime">Start Time</label>
              <input
                type="time"
                id="startTime"
                value={startTime}
                onChange={(e) => setStartTime(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="endTime">End Time</label>
              <input
                type="time"
                id="endTime"
                value={endTime}
                onChange={(e) => setEndTime(e.target.value)}
                required
              />
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="notes">Notes (optional)</label>
            <textarea
              id="notes"
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="Any special requirements or notes..."
              rows={3}
            />
          </div>

          <div className="modal-actions">
            <button type="button" className="btn btn-secondary" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? 'Booking...' : 'Confirm Booking'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
