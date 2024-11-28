document.getElementById('calculate').addEventListener('click', function() {
  const totalPrice = parseFloat(document.getElementById('total-price').value);
  const downPayment = parseFloat(document.getElementById('down-payment').value);
  const interestRate = parseFloat(document.getElementById('interest-rate').value);
  const loanYears = parseInt(document.getElementById('loan-years').value);
  const repaymentType = document.getElementById('repayment-type').value;

  // 计算贷款总数
  const loanAmount = totalPrice - downPayment;

  // 计算月付
  let monthlyPayment;
  if (repaymentType === '等额本息') {
    // 等额本息计算公式
    const monthlyInterestRate = interestRate / 12 / 100; // 利率转换为月利率
    const months = loanYears * 12;
    monthlyPayment = loanAmount * monthlyInterestRate * Math.pow(1 + monthlyInterestRate, months) / (Math.pow(1 + monthlyInterestRate, months) - 1);
  } else if (repaymentType === '等额本金') {
    // 等额本金计算公式
    const months = loanYears * 12;
    const principalPayment = loanAmount / months;
    monthlyPayment = principalPayment + (loanAmount - principalPayment) * (interestRate / 12 / 100);
  }

  // 显示结果
  document.getElementById('loan-amount').innerHTML = `贷款总数：${loanAmount}`;
  document.getElementById('monthly-payment').innerHTML = `月付：${monthlyPayment.toFixed(2)}`; // 保留两位小数
});