import { useState } from 'react';

interface SearchFilterProps {
  onSearch: (query: string) => void;
  onFilterType: (type: string) => void;
  onFilterBuilding: (building: string) => void;
  onReset: () => void;
}

export default function SearchFilter({ onSearch, onFilterType, onFilterBuilding, onReset }: SearchFilterProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedType, setSelectedType] = useState('');
  const [selectedBuilding, setSelectedBuilding] = useState('');

  const resourceTypes = [
    { value: '', label: 'All Types' },
    { value: 'meeting_room', label: 'Meeting Room' },
    { value: 'study_room', label: 'Study Room' },
    { value: 'computer_lab', label: 'Computer Lab' },
    { value: 'office', label: 'Office' },
    { value: 'library_desk', label: 'Library Desk' },
  ];

  const buildings = [
    { value: '', label: 'All Buildings' },
    { value: 'Main Building', label: 'Main Building' },
    { value: 'Science Building', label: 'Science Building' },
    { value: 'Library', label: 'Library' },
    { value: 'Engineering Building', label: 'Engineering Building' },
  ];

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch(searchQuery);
  };

  const handleTypeChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value;
    setSelectedType(value);
    onFilterType(value);
  };

  const handleBuildingChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value;
    setSelectedBuilding(value);
    onFilterBuilding(value);
  };

  const handleReset = () => {
    setSearchQuery('');
    setSelectedType('');
    setSelectedBuilding('');
    onReset();
  };

  return (
    <div className="search-filter">
      <form onSubmit={handleSearch} className="search-form">
        <div className="search-input-group">
          <input
            type="text"
            placeholder="Search resources..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="search-input"
          />
          <button type="submit" className="btn btn-primary">
            🔍 Search
          </button>
        </div>
      </form>

      <div className="filter-controls">
        <div className="filter-group">
          <label htmlFor="type-filter">Type:</label>
          <select
            id="type-filter"
            value={selectedType}
            onChange={handleTypeChange}
            className="filter-select"
          >
            {resourceTypes.map((type) => (
              <option key={type.value} value={type.value}>
                {type.label}
              </option>
            ))}
          </select>
        </div>

        <div className="filter-group">
          <label htmlFor="building-filter">Building:</label>
          <select
            id="building-filter"
            value={selectedBuilding}
            onChange={handleBuildingChange}
            className="filter-select"
          >
            {buildings.map((building) => (
              <option key={building.value} value={building.value}>
                {building.label}
              </option>
            ))}
          </select>
        </div>

        <button onClick={handleReset} className="btn btn-secondary">
          ↺ Reset
        </button>
      </div>
    </div>
  );
}
