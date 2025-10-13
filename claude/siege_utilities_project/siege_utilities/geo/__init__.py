"""
Geographic and Census data utilities for siege_utilities.
Provides comprehensive GIS and census data acquisition capabilities.
"""

# Import main census intelligence functions
from .census_data_selector import (
    get_census_data_selector,
    select_census_datasets,
    get_analysis_approach,
    select_datasets_for_analysis,
    get_dataset_compatibility_matrix,
    suggest_analysis_approach
)

from .census_dataset_mapper import (
    get_census_dataset_mapper,
    get_best_dataset_for_analysis,
    compare_census_datasets,
    get_dataset_info,
    list_datasets_by_type,
    list_datasets_by_geography,
    get_best_dataset_for_use_case,
    get_dataset_relationships,
    compare_datasets,
    get_data_selection_guide,
    export_dataset_catalog
)

from .spatial_data import (
    get_census_data,
    get_census_boundaries,
    download_osm_data,
    get_available_years,
    get_year_directory_contents,
    discover_boundary_types,
    construct_download_url,
    validate_download_url,
    get_optimal_year,
    download_data,
    get_geographic_boundaries,
    get_available_boundary_types,
    refresh_discovery_cache,
    get_available_state_fips,
    get_state_abbreviations,
    get_comprehensive_state_info,
    get_state_by_abbreviation,
    get_state_by_name,
    validate_state_fips,
    get_state_name,
    get_state_abbreviation,
    download_dataset,
    get_unified_fips_data,
    normalize_state_identifier_standalone,
    normalize_state_input,
    normalize_state_name,
    normalize_state_abbreviation,
    normalize_fips_code
)

from .geocoding import (
    concatenate_addresses,
    use_nominatim_geocoder
)

# Convenience functions for common workflows
def get_census_intelligence(*args, **kwargs):
    """
    High-level function to get census intelligence for a given use case.
    Wrapper around census_data_selector functionality.
    """
    selector = get_census_data_selector()
    return selector.get_intelligence(*args, **kwargs)


def quick_census_selection(use_case: str, geography: str = 'tract'):
    """
    Quick selection of census datasets for common use cases.

    Args:
        use_case: Description of analysis need
        geography: Geographic level (tract, block group, county, etc.)

    Returns:
        Recommended datasets and approach
    """
    mapper = get_census_dataset_mapper()
    return mapper.get_best_dataset_for_use_case(use_case, geography)


# Alias for backward compatibility
normalize_state_identifier = normalize_state_identifier_standalone

__all__ = [
    # Census Data Selection Intelligence
    'get_census_data_selector',
    'select_census_datasets',
    'get_analysis_approach',
    'select_datasets_for_analysis',
    'get_dataset_compatibility_matrix',
    'suggest_analysis_approach',

    # Census Dataset Mapping & Recommendations
    'get_census_dataset_mapper',
    'get_best_dataset_for_analysis',
    'compare_census_datasets',
    'get_dataset_info',
    'list_datasets_by_type',
    'list_datasets_by_geography',
    'get_best_dataset_for_use_case',
    'get_dataset_relationships',
    'compare_datasets',
    'get_data_selection_guide',
    'export_dataset_catalog',

    # Spatial Data & Boundary Downloads
    'get_census_data',
    'get_census_boundaries',
    'download_osm_data',
    'get_available_years',
    'get_year_directory_contents',
    'discover_boundary_types',
    'construct_download_url',
    'validate_download_url',
    'get_optimal_year',
    'download_data',
    'get_geographic_boundaries',
    'get_available_boundary_types',
    'refresh_discovery_cache',
    'get_available_state_fips',
    'get_state_abbreviations',
    'get_comprehensive_state_info',
    'get_state_by_abbreviation',
    'get_state_by_name',
    'validate_state_fips',
    'get_state_name',
    'get_state_abbreviation',
    'download_dataset',
    'get_unified_fips_data',
    'normalize_state_identifier',
    'normalize_state_identifier_standalone',
    'normalize_state_input',
    'normalize_state_name',
    'normalize_state_abbreviation',
    'normalize_fips_code',

    # Geocoding
    'concatenate_addresses',
    'use_nominatim_geocoder',

    # Convenience Functions
    'get_census_intelligence',
    'quick_census_selection'
]
