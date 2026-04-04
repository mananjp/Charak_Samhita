import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { herbsAPI } from '../../app/api';

// All 17 herbs from the Charaka Samhita reference list  
export const ALL_HERB_KEYS = [
  'ashwagandha', 'triphala', 'brahmi', 'tulsi', 'neem', 'shatavari',
  'giloy', 'amla', 'haritaki', 'bibhitaki', 'turmeric', 'ginger',
  'cumin', 'licorice', 'shankhapushpi', 'vidari', 'punarnava'
];

// Fetch names from API, then fall back to ALL_HERB_KEYS for any not returned
// Fetches full details for every herb in parallel
export const fetchAllHerbDetails = createAsyncThunk(
  'herbs/fetchAllDetails',
  async (_, { rejectWithValue }) => {
    try {
      // Get list from API (may not have all 17 if DB is partial)
      let apiKeys = [];
      try {
        const listRes = await herbsAPI.list();
        const data = listRes.data;
        apiKeys = Array.isArray(data) ? data : (data?.herbs || []);
      } catch (_) {
        apiKeys = [];
      }

      // Merge API keys with our known list (API keys first, then any extras from known list)
      const allKeys = [
        ...apiKeys.map(k => k.toLowerCase()),
        ...ALL_HERB_KEYS.filter(k => !apiKeys.map(a => a.toLowerCase()).includes(k))
      ];

      // Fetch all details in parallel
      const detailPromises = allKeys.map((name) =>
        herbsAPI.get(name)
          .then((r) => r.data)
          .catch(() => null)
      );
      const details = await Promise.all(detailPromises);
      return details.filter(Boolean); // remove any nulls
    } catch (err) {
      return rejectWithValue(err.response?.data?.detail || 'Failed to load herbs');
    }
  }
);

export const fetchHerbDetail = createAsyncThunk('herbs/fetchDetail', async (name, { rejectWithValue }) => {
  try {
    const res = await herbsAPI.get(name);
    return res.data;
  } catch (err) {
    return rejectWithValue(err.response?.data?.detail || 'Herb not found');
  }
});

const herbsSlice = createSlice({
  name: 'herbs',
  initialState: {
    list: [],
    selected: null,
    filter: '',
    loading: false,
    error: null,
  },
  reducers: {
    setFilter: (state, action) => { state.filter = action.payload; },
    setSelected: (state, action) => { state.selected = action.payload; },
    clearSelected: (state) => { state.selected = null; },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchAllHerbDetails.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllHerbDetails.fulfilled, (state, action) => {
        state.loading = false;
        state.list = action.payload;
      })
      .addCase(fetchAllHerbDetails.rejected, (state, action) => { state.loading = false; state.error = action.payload; })
      .addCase(fetchHerbDetail.fulfilled, (state, action) => { state.selected = action.payload; });
  },
});

export const { setFilter, setSelected, clearSelected } = herbsSlice.actions;
export default herbsSlice.reducer;
