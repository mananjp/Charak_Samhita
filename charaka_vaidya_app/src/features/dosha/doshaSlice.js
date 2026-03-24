import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { doshaAPI } from '../../app/api';

export const assessDosha = createAsyncThunk('dosha/assess', async (answers, { rejectWithValue }) => {
  try {
    const res = await doshaAPI.assess(answers);
    return res.data;
  } catch (err) {
    return rejectWithValue(err.response?.data?.detail || 'Assessment failed');
  }
});

const doshaSlice = createSlice({
  name: 'dosha',
  initialState: {
    answers: {},
    result: null,
    currentStep: 0,
    loading: false,
    error: null,
  },
  reducers: {
    setAnswer: (state, action) => {
      const { questionId, answer } = action.payload;
      state.answers[questionId] = answer;
    },
    nextStep: (state) => { state.currentStep += 1; },
    prevStep: (state) => { state.currentStep = Math.max(0, state.currentStep - 1); },
    resetQuiz: (state) => {
      state.answers = {};
      state.result = null;
      state.currentStep = 0;
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(assessDosha.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(assessDosha.fulfilled, (state, action) => { state.loading = false; state.result = action.payload; })
      .addCase(assessDosha.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { setAnswer, nextStep, prevStep, resetQuiz } = doshaSlice.actions;
export default doshaSlice.reducer;
