import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { useAuth } from '../context/AuthContext';
import type { Resource, Reservation } from '../types';
import { resourceService } from '../services/resourceService';
import { reservationService } from '../services/reservationService';
import ResourceCard from '../components/ResourceCard';
import ReservationList from '../components/ReservationList';
import BookingModal from '../components/BookingModal';
import SearchFilter from '../components/SearchFilter';
import ReservationFilters from '../components/ReservationFilters';

export default function Dashboard() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [resources, setResources] = useState<Resource[]>([]);
  const [allResources, setAllResources] = useState<Resource[]>([]);
  const [reservations, setReservations] = useState<Reservation[]>([]);
  const [allReservations, setAllReservations] = useState<Reservation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedResource, setSelectedResource] = useState<Resource | null>(null);
  const [showBookingModal, setShowBookingModal] = useState(false);
  const [activeTab, setActiveTab] = useState<'resources' | 'reservations'>('resources');

  useEffect(() => {
    let isMounted = true;
    
    const loadData = async () => {
      try {
        const [resourcesData, reservationsData] = await Promise.all([
          resourceService.getAll().catch((err) => {
            console.error('Resources fetch error:', err);
            return [];
          }),
          reservationService.getMyReservations().catch((err) => {
            console.error('Reservations fetch error:', err);
            return [];
          }),
        ]);
        
        if (isMounted) {
          setResources(resourcesData);
          setAllResources(resourcesData);
          setReservations(reservationsData);
          setAllReservations(reservationsData);
          setLoading(false);
        }
      } catch (err) {
        console.error('Load data error:', err);
        if (isMounted) {
          setError('Failed to load data. Please try again.');
          setLoading(false);
        }
      }
    };

    loadData();
    
    return () => {
      isMounted = false;
    };
  }, []);

  const refreshData = async () => {
    setLoading(true);
    try {
      const [resourcesData, reservationsData] = await Promise.all([
        resourceService.getAll().catch(() => []),
        reservationService.getMyReservations().catch(() => []),
      ]);
      setResources(resourcesData);
      setAllResources(resourcesData);
      setReservations(reservationsData);
      setAllReservations(reservationsData);
    } catch (err) {
      console.error('Refresh error:', err);
    } finally {
      setLoading(false);
    }
  };

  // Search and filter handlers for resources
  const handleSearch = async (query: string) => {
    if (!query.trim()) {
      setResources(allResources);
      return;
    }
    try {
      const results = await resourceService.search(query);
      setResources(results);
    } catch (err) {
      toast.error('Search failed');
    }
  };

  const handleFilterType = async (type: string) => {
    if (!type) {
      setResources(allResources);
      return;
    }
    try {
      const results = await resourceService.getFiltered({ resource_type: type });
      setResources(results);
    } catch (err) {
      console.error('Filter error:', err);
      toast.error('Filter failed');
    }
  };

  const handleFilterBuilding = async (building: string) => {
    if (!building) {
      setResources(allResources);
      return;
    }
    try {
      const results = await resourceService.getFiltered({ building });
      setResources(results);
    } catch (err) {
      console.error('Filter error:', err);
      toast.error('Filter failed');
    }
  };

  const handleResetResourceFilters = () => {
    setResources(allResources);
  };

  // Filter handlers for reservations
  const handleFilterReservationStatus = (status: string) => {
    if (!status) {
      setReservations(allReservations);
      return;
    }
    const filtered = allReservations.filter(r => r.status === status);
    setReservations(filtered);
  };

  const handleFilterReservationDateRange = (startDate: string, endDate: string) => {
    let filtered = allReservations;
    
    if (startDate) {
      filtered = filtered.filter(r => r.date >= startDate);
    }
    if (endDate) {
      filtered = filtered.filter(r => r.date <= endDate);
    }
    
    setReservations(filtered);
  };

  const handleResetReservationFilters = () => {
    setReservations(allReservations);
  };

  const handleBookResource = (resource: Resource) => {
    setSelectedResource(resource);
    setShowBookingModal(true);
  };

  const handleBookingComplete = () => {
    setShowBookingModal(false);
    setSelectedResource(null);
    refreshData();
  };

  const handleCancelReservation = async (id: string) => {
    const reservation = reservations.find(r => r.id === id);
    const loadingToast = toast.loading('Cancelling reservation...');
    
    try {
      await reservationService.cancel(id);
      toast.success(
        `Reservation ${reservation?.resource_name ? `for ${reservation.resource_name}` : ''} cancelled successfully`,
        { id: loadingToast, icon: '✅' }
      );
      refreshData();
    } catch (err) {
      console.error('Failed to cancel reservation:', err);
      const errorMessage = err instanceof Error ? err.message : 'Failed to cancel reservation';
      toast.error(errorMessage, { id: loadingToast, icon: '❌' });
    }
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div className="header-content">
          <h1>🏢 Reservation System</h1>
          <div className="user-info">
            <button 
              onClick={() => navigate('/profile')} 
              className="btn btn-link profile-link"
              title="View Profile"
            >
              👤 {user?.full_name || user?.username}
            </button>
            <span className="role-badge">{user?.role}</span>
            <button onClick={logout} className="btn btn-secondary">
              Logout
            </button>
          </div>
        </div>
      </header>

      <nav className="dashboard-nav">
        <button
          className={`tab-btn ${activeTab === 'resources' ? 'active' : ''}`}
          onClick={() => setActiveTab('resources')}
        >
          📚 Available Resources
        </button>
        <button
          className={`tab-btn ${activeTab === 'reservations' ? 'active' : ''}`}
          onClick={() => setActiveTab('reservations')}
        >
          📅 My Reservations
        </button>
      </nav>

      <main className="dashboard-content">
        {loading ? (
          <div className="loading">Loading...</div>
        ) : error ? (
          <div className="error-message">{error}</div>
        ) : (
          <>
            {activeTab === 'resources' && (
              <div className="resources-section">
                <h2>Available Resources</h2>
                <SearchFilter
                  onSearch={handleSearch}
                  onFilterType={handleFilterType}
                  onFilterBuilding={handleFilterBuilding}
                  onReset={handleResetResourceFilters}
                />
                {resources.length === 0 ? (
                  <p className="empty-message">No resources available at the moment.</p>
                ) : (
                  <div className="resources-grid">
                    {resources.map((resource) => (
                      <ResourceCard
                        key={resource.id}
                        resource={resource}
                        onBook={handleBookResource}
                      />
                    ))}
                  </div>
                )}
              </div>
            )}

            {activeTab === 'reservations' && (
              <div className="reservations-section">
                <h2>My Reservations</h2>
                <ReservationFilters
                  onFilterStatus={handleFilterReservationStatus}
                  onFilterDateRange={handleFilterReservationDateRange}
                  onReset={handleResetReservationFilters}
                />
                <ReservationList
                  reservations={reservations}
                  onCancel={handleCancelReservation}
                />
              </div>
            )}
          </>
        )}
      </main>

      {showBookingModal && selectedResource && (
        <BookingModal
          resource={selectedResource}
          onClose={() => setShowBookingModal(false)}
          onComplete={handleBookingComplete}
        />
      )}
    </div>
  );
}
