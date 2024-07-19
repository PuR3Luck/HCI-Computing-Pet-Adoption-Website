function setupDoubleSlider(minSlider, maxSlider, minValue, maxValue, hiddenMin, hiddenMax) {
  const range = minSlider.parentElement.querySelector('.slider-range');
  
  function updateSliderValues() {
    const min = Math.min(parseInt(minSlider.value), parseInt(maxSlider.value) - 1);
    const max = Math.max(parseInt(maxSlider.value), parseInt(minSlider.value) + 1);

    minSlider.value = min;
    maxSlider.value = max;

    minValue.textContent = min;
    maxValue.textContent = max;

    hiddenMin.value = min;
    hiddenMax.value = max;

    updateSliderRange(minSlider, maxSlider, range);
  }

  minSlider.oninput = maxSlider.oninput = updateSliderValues;
  updateSliderValues();
}

function updateSliderRange(minSlider, maxSlider, range) {
  const min = parseInt(minSlider.value);
  const max = parseInt(maxSlider.value);
  const percent1 = (min / parseInt(minSlider.max)) * 100;
  const percent2 = (max / parseInt(maxSlider.max)) * 100;
  range.style.left = percent1 + "%";
  range.style.width = (percent2 - percent1) + "%";
}

function updateAgeLimits() {
  const minLimit = parseInt(document.getElementById('age-min-limit').value);
  const maxLimit = parseInt(document.getElementById('age-max-limit').value);
  
  if (minLimit >= maxLimit) {
    alert('Minimum age must be less than maximum age');
    return;
  }

  const minSlider = document.getElementById('min-age-slider');
  const maxSlider = document.getElementById('max-age-slider');

  minSlider.min = maxSlider.min = minLimit;
  minSlider.max = maxSlider.max = maxLimit;

  setupDoubleSlider(
    minSlider,
    maxSlider,
    document.getElementById('min-age-value'),
    document.getElementById('max-age-value'),
    document.getElementById('min-age'),
    document.getElementById('max-age')
  );
}

function updateFeeLimits() {
  const minLimit = parseInt(document.getElementById('fee-min-limit').value);
  const maxLimit = parseInt(document.getElementById('fee-max-limit').value);
  
  if (minLimit >= maxLimit) {
    alert('Minimum fee must be less than maximum fee');
    return;
  }

  const minSlider = document.getElementById('min-fee-slider');
  const maxSlider = document.getElementById('max-fee-slider');

  minSlider.min = maxSlider.min = minLimit;
  minSlider.max = maxSlider.max = maxLimit;

  setupDoubleSlider(
    minSlider,
    maxSlider,
    document.getElementById('min-fee-value'),
    document.getElementById('max-fee-value'),
    document.getElementById('min-fee'),
    document.getElementById('max-fee')
  );
}

// Initial setup
setupDoubleSlider(
  document.getElementById('min-age-slider'),
  document.getElementById('max-age-slider'),
  document.getElementById('min-age-value'),
  document.getElementById('max-age-value'),
  document.getElementById('min-age'),
  document.getElementById('max-age')
);

setupDoubleSlider(
  document.getElementById('min-fee-slider'),
  document.getElementById('max-fee-slider'),
  document.getElementById('min-fee-value'),
  document.getElementById('max-fee-value'),
  document.getElementById('min-fee'),
  document.getElementById('max-fee')
);