document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('purchaseForm');
    const dateInput = document.getElementById('date');
    const billNoInput = document.getElementById('bill_no');
    const clearBtn = document.getElementById('clearBtn');

    const bags = document.getElementById('bags');
    const netWeightKg = document.getElementById('net_weight_kg');
    const gunnyWeightKg = document.getElementById('gunny_weight_kg');
    const finalWeightKg = document.getElementById('final_weight_kg');
    const weightQuintal = document.getElementById('weight_quintal');
    const weightKhandi = document.getElementById('weight_khandi');
    const avgBagWeight = document.getElementById('avg_bag_weight');
    const rateBasis = document.getElementById('rate_basis');
    const rateValue = document.getElementById('rate_value');
    const totalPurchaseAmount = document.getElementById('total_purchase_amount');
    const bankCommission = document.getElementById('bank_commission');
    const postage = document.getElementById('postage');
    const freight = document.getElementById('freight');
    const rateDiff = document.getElementById('rate_diff');
    const qualityDiff = document.getElementById('quality_diff');
    const moistureDed = document.getElementById('moisture_ded');
    const tds = document.getElementById('tds');
    const batavPercent = document.getElementById('batav_percent');
    const batav = document.getElementById('batav');
    const dalaliRate = document.getElementById('dalali_rate');
    const dalali = document.getElementById('dalali');
    const hammaliRate = document.getElementById('hammali_rate');
    const hammali = document.getElementById('hammali');
    const totalDeduction = document.getElementById('total_deduction');
    const payableAmount = document.getElementById('payable_amount');
    const paymentAmount = document.getElementById('payment_amount');

    dateInput.valueAsDate = new Date();
    fetchNextBillNo();

    function fetchNextBillNo() {
        fetch('/api/next-bill-no')
            .then(response => response.json())
            .then(data => {
                billNoInput.value = data.bill_no;
            })
            .catch(error => {
                console.error('Error fetching bill number:', error);
                billNoInput.value = '1';
            });
    }

    function calculateWeightFields() {
        const netKg = parseFloat(netWeightKg.value) || 0;
        const gunnyKg = parseFloat(gunnyWeightKg.value) || 0;
        const bagsVal = parseFloat(bags.value) || 0;

        const finalKg = Math.max(0, netKg - gunnyKg);
        const quintal = finalKg / 100;
        const khandi = finalKg / 150;
        const avgBag = bagsVal > 0 ? (finalKg / bagsVal) : 0;

        finalWeightKg.value = finalKg.toFixed(2);
        weightQuintal.value = quintal.toFixed(3);
        weightKhandi.value = khandi.toFixed(3);
        avgBagWeight.value = avgBag.toFixed(2);

        return { finalKg, quintal, khandi };
    }

    function calculateTotalPurchaseAmount() {
        const weights = calculateWeightFields();
        const rateBasisVal = rateBasis.value;
        const rateVal = parseFloat(rateValue.value) || 0;

        let totalAmount = 0;
        if (rateBasisVal === 'Quintal') {
            totalAmount = weights.quintal * rateVal;
        } else if (rateBasisVal === 'Khandi') {
            totalAmount = weights.khandi * rateVal;
        }

        totalPurchaseAmount.value = totalAmount.toFixed(2);
        return totalAmount;
    }

    function calculateFields() {
        const totalAmount = calculateTotalPurchaseAmount();
        const rateBasisVal = rateBasis.value;
        const quintal = parseFloat(weightQuintal.value) || 0;
        const khandi = parseFloat(weightKhandi.value) || 0;

        const bankCommissionVal = parseFloat(bankCommission.value) || 0;
        const postageVal = parseFloat(postage.value) || 0;
        const freightVal = parseFloat(freight.value) || 0;
        const rateDiffVal = parseFloat(rateDiff.value) || 0;
        const qualityDiffVal = parseFloat(qualityDiff.value) || 0;
        const moistureDedVal = parseFloat(moistureDed.value) || 0;
        const tdsVal = parseFloat(tds.value) || 0;

        const batavPercentVal = parseFloat(batavPercent.value) || 0;
        const dalaliRateVal = parseFloat(dalaliRate.value) || 0;
        const hammaliRateVal = parseFloat(hammaliRate.value) || 0;

        const batavVal = batavPercentVal > 0 ? (totalAmount * (batavPercentVal / 100)) : 0;

        // NEW: Dalali & Hammali based on selected Rate Basis
        let dalaliVal = 0;
        let hammaliVal = 0;
        if (rateBasisVal === 'Quintal') {
            dalaliVal = dalaliRateVal > 0 ? (quintal * dalaliRateVal) : 0;
            hammaliVal = hammaliRateVal > 0 ? (quintal * hammaliRateVal) : 0;
        } else if (rateBasisVal === 'Khandi') {
            dalaliVal = dalaliRateVal > 0 ? (khandi * dalaliRateVal) : 0;
            hammaliVal = hammaliRateVal > 0 ? (khandi * hammaliRateVal) : 0;
        }

        const categoryADeductions = bankCommissionVal + postageVal + freightVal + rateDiffVal + qualityDiffVal + moistureDedVal + tdsVal;
        const totalDeductionVal = categoryADeductions + batavVal + dalaliVal + hammaliVal;

        const payableAmountVal = totalAmount - totalDeductionVal;

        batav.value = batavVal.toFixed(2);
        dalali.value = dalaliVal.toFixed(2);
        hammali.value = hammaliVal.toFixed(2);
        totalDeduction.value = totalDeductionVal.toFixed(2);
        payableAmount.textContent = payableAmountVal.toFixed(2);
        paymentAmount.value = payableAmountVal.toFixed(2);
    }

    netWeightKg.addEventListener('input', calculateFields);
    gunnyWeightKg.addEventListener('input', calculateFields);
    bags.addEventListener('input', calculateFields);
    rateBasis.addEventListener('change', calculateFields);
    rateValue.addEventListener('input', calculateFields);

    document.querySelectorAll('.calc-input').forEach(input => {
        input.addEventListener('input', calculateFields);
    });

    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        const formData = new FormData(form);
        const data = {};

        formData.forEach((value, key) => {
            data[key] = value;
        });

        data['net_weight_kg'] = netWeightKg.value;
        data['gunny_weight_kg'] = gunnyWeightKg.value;
        data['final_weight_kg'] = finalWeightKg.value;
        data['weight_quintal'] = weightQuintal.value;
        data['weight_khandi'] = weightKhandi.value;
        data['avg_bag_weight'] = avgBagWeight.value;
        data['rate_basis'] = rateBasis.value;
        data['rate_value'] = rateValue.value;
        data['total_purchase_amount'] = totalPurchaseAmount.value;
        data['batav'] = batav.value;
        data['dalali'] = dalali.value;
        data['hammali'] = hammali.value;
        data['total_deduction'] = totalDeduction.value;
        data['payable_amount'] = payableAmount.textContent;

        try {
            const response = await fetch('/api/add-slip', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`Server error: ${response.status} - ${errorText}`);
            }

            const result = await response.json();

            if (result.success) {
                alert('Purchase slip saved successfully!');
                window.open(`/print/${result.slip_id}`, '_blank');
                form.reset();
                dateInput.valueAsDate = new Date();
                fetchNextBillNo();
                calculateFields();
            } else {
                alert('Error saving slip: ' + result.message);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error saving purchase slip: ' + error.message);
        }
    });

    clearBtn.addEventListener('click', function() {
        if (confirm('Are you sure you want to clear the form?')) {
            form.reset();
            dateInput.valueAsDate = new Date();
            fetchNextBillNo();
            calculateFields();
        }
    });

    calculateCalculatedRate();
    calculateFields();

    // ===== DYNAMIC GODOWN DROPDOWN =====
    const godownInput = document.getElementById('paddy_unloading_godown');
    const godownDatalist = document.getElementById('godownList');
    const saveGodownBtn = document.getElementById('saveGodownBtn');
    let allGodowns = [];

    // Load existing godowns on page load
    async function loadGodowns() {
        try {
            const response = await fetch('/api/unloading-godowns');
            const result = await response.json();

            if (result.success) {
                allGodowns = result.godowns;
                updateGodownDatalist();
                console.log(`✓ Loaded ${allGodowns.length} godowns`);
            }
        } catch (error) {
            console.error('Error loading godowns:', error);
        }
    }

    // Update datalist with godown options
    function updateGodownDatalist() {
        godownDatalist.innerHTML = '';
        allGodowns.forEach(godown => {
            const option = document.createElement('option');
            option.value = godown.name;
            godownDatalist.appendChild(option);
        });
    }

    // Save new godown when button is clicked
    async function saveNewGodown() {
        const enteredValue = godownInput.value.trim();

        if (!enteredValue) {
            alert('Please enter a godown name');
            return;
        }

        // Check if it already exists in the list
        const exists = allGodowns.some(g => g.name.toLowerCase() === enteredValue.toLowerCase());

        if (exists) {
            alert('This godown already exists in the list');
            return;
        }

        // Add new godown to database
        try {
            saveGodownBtn.disabled = true;
            saveGodownBtn.textContent = 'Saving...';

            const response = await fetch('/api/unloading-godowns', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ name: enteredValue })
            });

            const result = await response.json();

            if (result.success) {
                console.log(`✓ Added new godown: ${enteredValue}`);
                allGodowns = result.godowns; // Update with new list from server
                updateGodownDatalist();
                alert(`Godown "${enteredValue}" saved successfully!`);
                // Keep the value selected in the input
            } else {
                alert('Error saving godown: ' + result.message);
            }
        } catch (error) {
            console.error('Error adding godown:', error);
            alert('Error saving godown. Please try again.');
        } finally {
            saveGodownBtn.disabled = false;
            saveGodownBtn.textContent = 'Save New Godown';
        }
    }

    // Attach click event to Save button
    saveGodownBtn.addEventListener('click', saveNewGodown);

    // Load godowns when page loads
    loadGodowns();
});

// ===== DYNAMIC INSTALMENT MANAGEMENT =====
let visibleInstalments = [1]; // Track which instalments are shown

function addInstalment() {
    // Find next hidden instalment
    for (let i = 2; i <= 5; i++) {
        if (!visibleInstalments.includes(i)) {
            const card = document.getElementById(`instalment_${i}_card`);
            if (card) {
                card.style.display = 'block';
                visibleInstalments.push(i);
            }
            break;
        }
    }

    // Hide add button if all 5 are visible
    if (visibleInstalments.length >= 5) {
        document.getElementById('addInstalmentBtn').style.display = 'none';
    }
}

function removeInstalment(num) {
    const card = document.getElementById(`instalment_${num}_card`);
    if (card) {
        card.style.display = 'none';

        // Clear all fields
        document.getElementById(`instalment_${num}_date`).value = '';
        document.getElementById(`instalment_${num}_amount`).value = '0';
        document.getElementById(`instalment_${num}_payment_method`).value = '';
        document.getElementById(`instalment_${num}_payment_bank_account`).value = '';
        document.getElementById(`instalment_${num}_comment`).value = '';

        // Remove from visible list
        visibleInstalments = visibleInstalments.filter(i => i !== num);

        // Show add button again
        document.getElementById('addInstalmentBtn').style.display = 'inline-block';
    }
}
