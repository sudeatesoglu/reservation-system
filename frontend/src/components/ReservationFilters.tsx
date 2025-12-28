import { useState } from 'react';

interface ReservationFiltersProps {
  onFilterStatus: (status: string) => void;
  onFilterDateRange: (startDate: string, endDate: string) => void;
  onReset: () => void;
}

export default function ReservationFilters({ onFilterStatus, onFilterDateRange, onReset }: ReservationFiltersProps) {
  const [selectedStatus, setSelectedStatus] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');

  const statuses = [
    { value: '', label: 'All Statuses' },
    { value: 'confirmed', label: 'Confirmed' },
    { value: 'pending', label: 'Pending' },
    { value: 'cancelled', label: 'Cancelled' },
    { value: 'completed', label: 'Completed' },
  ];

  const handleStatusChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value;
    setSelectedStatus(value);
    onFilterStatus(value);
  };

  const handleDateFilter = () => {
    if (startDate || endDate) {
      onFilterDateRange(startDate, endDate);
    }
  };

  const handleReset = () => {
    setSelectedStatus('');
    setStartDate('');
    setEndDate('');
    onReset();
  };

  return (
    <div className="reservation-filters">
      <div className="filter-controls">
        <div className="filter-group">
          <label htmlFor="status-filter">Status:</label>
          <select
            id="status-filter"
            value={selectedStatus}
            onChange={handleStatusChange}
            className="filter-select"
          >
            {statuses.map((status) => (
              <option key={status.value} value={status.value}>
                {status.label}
              </option>
            ))}
          </select>
        </div>

        <div className="filter-group">
          <label htmlFor="start-date">From:</label>
          <input
            type="date"
            id="start-date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            className="date-input"
          />
        </div>

        <div className="filter-group">
          <label htmlFor="end-date">To:</label>
          <input
            type="date"
            id="end-date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            className="date-input"
          />
        </div>

        <button onClick={handleDateFilter} className="btn btn-primary">
          Apply Date
        </button>

        <button onClick={handleReset} className="btn btn-secondary">
          ↺ Reset
        </button>
      </div>
    </div>
  );
}
