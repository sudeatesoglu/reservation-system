import type { Resource } from '../types';

interface ResourceCardProps {
  resource: Resource;
  onBook: (resource: Resource) => void;
}

export default function ResourceCard({ resource, onBook }: ResourceCardProps) {
  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'meeting_room':
        return '🏢';
      case 'study_room':
        return '📚';
      case 'computer_lab':
        return '💻';
      case 'office':
        return '🏠';
      case 'library_desk':
        return '🪑';
      default:
        return '📦';
    }
  };

  const getTypeLabel = (type: string) => {
    return type.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
  };

  const isAvailable = resource.status === 'available';

  return (
    <div className="resource-card">
      <div className="resource-icon">{getTypeIcon(resource.resource_type)}</div>
      <div className="resource-info">
        <h3>{resource.name}</h3>
        <p className="resource-type">{getTypeLabel(resource.resource_type)}</p>
        {resource.description && (
          <p className="resource-description">{resource.description}</p>
        )}
        <div className="resource-details">
          <span className="detail">
            👥 Capacity: {resource.capacity}
          </span>
          {resource.location && (
            <span className="detail">
              📍 {resource.location}
            </span>
          )}
        </div>
        {resource.amenities && resource.amenities.length > 0 && (
          <div className="amenities">
            {resource.amenities.map((amenity, index) => (
              <span key={index} className="amenity-tag">
                {amenity}
              </span>
            ))}
          </div>
        )}
      </div>
      <button
        className="btn btn-primary"
        onClick={() => onBook(resource)}
        disabled={!isAvailable}
      >
        {isAvailable ? 'Book Now' : 'Unavailable'}
      </button>
    </div>
  );
}
