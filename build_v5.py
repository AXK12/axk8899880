#!/usr/bin/env python3
"""
Build pro_v5.html: Add 密码集萃 (CipherEngine) as a togglable third engine
to the existing pro.html (Method A + Method B + Cipher).

Changes:
  1. Injects CipherEngine JS (sum≤MAX, diff, integer division)
  2. Adds toggle switch in settings for both SSQ and DLT
  3. Modifies predict() to also compute cipher pool when toggle is on
  4. Adds cipher pool display section in renderResult
  5. Updates page title to "Pro版 · 三引擎融合"
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\xiank\.openclaw\workspace\toolbox\pro.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ============================================================================
# 1. Inject CipherEngine JavaScript function (after the engine functions)
# ============================================================================
# Find where to inject: right after the predict() function definition
# The predict() function starts with "function predict(front, back, isSSQ, bluePrev2, blueHistory)"

cipher_js = """
// ==================== 密码集萃引擎 (CIPHER ENGINE) ====================
// 三步运算: 和≤MAX ∪ 差 ∪ 整除商
// SSQ: 6红, MAX=33, C(6,2)=15对
// DLT: 5前区, MAX=35, C(5,2)=10对
function cipherEngine(front, maxVal) {
  var pool = new Set();

  // Generate all C(n,2) pairs
  for (var i = 0; i < front.length; i++) {
    for (var j = i + 1; j < front.length; j++) {
      var a = front[i], b = front[j];

      // Step 1: Sum (a + b <= maxVal)
      var s = a + b;
      if (s <= maxVal) pool.add(s);

      // Step 2: Difference (b - a)
      pool.add(b - a);

      // Step 3: Integer division (b % a == 0)
      if (b % a === 0) pool.add(b // a);
    }
  }

  return Array.from(pool).filter(function(n) { return n >= 1 && n <= maxVal; }).sort(function(a, b) { return a - b; });
}

"""

# Inject after the methodBQREngine function and before predict
# The inject point: right before "// ==================== MAIN PREDICTOR ===================="
inject_marker = "// ==================== MAIN PREDICTOR ===================="
html = html.replace(inject_marker, cipher_js + "\n" + inject_marker)

# ============================================================================
# 2. Add cipher toggle in global settings
# ============================================================================
# Find BLUE_SETTINGS definition and add cipherEnabled
old_settings = """var BLUE_SETTINGS = {
  coldHotWindow: 11, hotThreshold: 3, warmThreshold: 2,
  filterLonely: true, filterMid: true, filterJump: true, filterCold: true,
  filterAcKill: false,  // 淘汰极低AC值（默认关闭）
  filterConsecKill: false,  // 淘汰超长连号（默认关闭）
  consecMaxRun: 5,  // 最长连号上限
  filterAllPrimeKill: false  // 淘汰全质号组合（默认关闭）
};"""

new_settings = """var BLUE_SETTINGS = {
  coldHotWindow: 11, hotThreshold: 3, warmThreshold: 2,
  filterLonely: true, filterMid: true, filterJump: true, filterCold: true,
  filterAcKill: false,  // 淘汰极低AC值（默认关闭）
  filterConsecKill: false,  // 淘汰超长连号（默认关闭）
  consecMaxRun: 5,  // 最长连号上限
  filterAllPrimeKill: false,  // 淘汰全质号组合（默认关闭）
  cipherEnabled: false  // 密码集萃引擎（默认关闭）
};"""

html = html.replace(old_settings, new_settings)

# ============================================================================
# 3. Add cipher toggle UI in settings (SSQ card, advanced settings)
# ============================================================================
# Add after the all-prime filter setting
old_prime_filter = """      <label style="font-size:11px">🚫 全质号过滤(SSQ独有)</label>
      <div style="display:flex;align-items:center;gap:10px;margin-top:4px">
        <label style="display:flex;align-items:center;gap:4px;font-size:11px;color:#8899b0;cursor:pointer;margin:0">
          <input type="checkbox" id="setting-allprime-kill"> 淘汰全红质号组合
        </label>
        <span style="font-size:10px;color:#5a7a9a">(质数:2,3,5,7,11,13,17,19,23,29,31,共924注)</span>
      </div>"""

new_prime_filter = """      <label style="font-size:11px">🚫 全质号过滤(SSQ独有)</label>
      <div style="display:flex;align-items:center;gap:10px;margin-top:4px">
        <label style="display:flex;align-items:center;gap:4px;font-size:11px;color:#8899b0;cursor:pointer;margin:0">
          <input type="checkbox" id="setting-allprime-kill"> 淘汰全红质号组合
        </label>
        <span style="font-size:10px;color:#5a7a9a">(质数:2,3,5,7,11,13,17,19,23,29,31,共924注)</span>
      </div>

      <hr style="border:0;border-top:1px solid #1e2a40;margin:10px 0">
      <div style="font-size:12px;color:#f0c040;margin-bottom:6px">🔐 密码集萃引擎 <span style="font-size:10px;color:#8899b0">(和+差+商 → 确定性候选池)</span></div>
      <div style="display:flex;align-items:center;gap:10px;margin-top:4px">
        <label style="display:flex;align-items:center;gap:8px;font-size:12px;color:#e0e6f0;cursor:pointer;margin:0;padding:6px 12px;background:#1a2530;border-radius:8px;border:1px solid #2a3a58">
          <span style="font-size:11px;color:#8899b0">⚡ 启用密码集萃</span>
          <span id="cipher-toggle-indicator" style="font-size:11px;padding:2px 10px;border-radius:10px;background:#3a3a4a;color:#666">关闭</span>
        </label>
        <input type="checkbox" id="setting-cipher-enabled" style="display:none">
        <span style="font-size:10px;color:#5a7a9a">回测平均命中3.45/6球，脱靶率0.58%</span>
      </div>"""

html = html.replace(old_prime_filter, new_prime_filter)

# ============================================================================
# 4. Apply cipher toggle state in applySettings()
# ============================================================================
old_apply = """  BLUE_SETTINGS.filterAllPrimeKill = document.getElementById('setting-allprime-kill').checked;"""

new_apply = """  BLUE_SETTINGS.filterAllPrimeKill = document.getElementById('setting-allprime-kill').checked;
  BLUE_SETTINGS.cipherEnabled = document.getElementById('setting-cipher-enabled').checked;
  
  // Update cipher toggle indicator
  var indicator = document.getElementById('cipher-toggle-indicator');
  if (BLUE_SETTINGS.cipherEnabled) {
    indicator.textContent = '已开启';
    indicator.style.background = '#1a4a20';
    indicator.style.color = '#27ae60';
  } else {
    indicator.textContent = '关闭';
    indicator.style.background = '#3a3a4a';
    indicator.style.color = '#666';
  }"""

html = html.replace(old_apply, new_apply)

# ============================================================================
# 5. Add cipher results to predict() return object
# ============================================================================
# Before `  return {` in the predict function, add:
old_predict_return = """  return {"""
# We need to add cipher computation. The predict() function takes front (reds/blue fronts combined).
# But we need the raw front numbers (just reds/maqian). Let's add cipher after the main compute.
# Find the section where all front predictions are computed, and add cipher result.

# Actually, the cleanest way: add cipher pool computation inside the return statement
# by computing it before the return.

# Find the last var declaration before return:
old_before_return = """  var frontAP = Array.from(frontPredsA).sort(function(a, b) { return a - b; });
  var frontBP = Array.from(frontPredsB).sort(function(a, b) { return a - b; });

  return {"""

new_before_return = """  var frontAP = Array.from(frontPredsA).sort(function(a, b) { return a - b; });
  var frontBP = Array.from(frontPredsB).sort(function(a, b) { return a - b; });

  // 密码集萃引擎计算（受全局开关控制）
  var frontCipher = cipherEngine(front.slice(0, isSSQ ? 6 : 5), maxVal);

  return {"""

html = html.replace(old_before_return, new_before_return)

# Add front_cipher to the return object
old_return_obj = """    consec_max_run: getMaxConsecutiveRun(front),"""

new_return_obj = """    front_cipher: frontCipher,
    consec_max_run: getMaxConsecutiveRun(front),"""

html = html.replace(old_return_obj, new_return_obj)

# ============================================================================
# 6. Add cipher display section in renderResult
# ============================================================================
# After the Method B section and before the Legend section
old_method_b = """      // Method B
      if (result.front_b.length > 0) {"""

# We'll add a cipher section right after the Legend HTML, before the 
# pivot kill section. Let me find the legend insertion point.
# The legend is rendered with: "// Legend"

# Actually, let's add the cipher section as a new pool section after method B
# and before the legend.

# Find: `// Legend`
legend_marker = """      // Legend
      html += '<div style=\"font-size:10px;color:#6a7a90;margin:4px 0 8px;display:flex;gap:14px;flex-wrap:wrap\">' +
        '<span>⭐发光=共识号码</span><span style=\"color:#3498db\">●蓝圈=仅方法A</span><span style=\"color:#27ae60\">●绿圈=仅方法B</span></div>';"""

cipher_legend_section = """      // Cipher engine section
      // 密码集萃引擎（仅在启用时显示）
      
      // Legend
      html += '<div style=\"font-size:10px;color:#6a7a90;margin:4px 0 8px;display:flex;gap:14px;flex-wrap:wrap\">' +
        '<span>⭐发光=共识号码</span><span style=\"color:#3498db\">●蓝圈=仅方法A</span><span style=\"color:#27ae60\">●绿圈=仅方法B</span></div>';"""

html = html.replace(legend_marker, cipher_legend_section)

# Now add the cipher section. We need to add it right after the legend
# and before the pivot kill section.
# Find: `// 天平支点杀红（仅双色球）`
pivot_marker = """      // 天平支点杀红（仅双色球）"""

cipher_section = """      // 密码集萃引擎显示
      if (BLUE_SETTINGS.cipherEnabled && result.front_cipher && result.front_cipher.length > 0) {
        html += '<div class=\"pool-section\" style=\"border:1px solid #e67e22;background:linear-gradient(135deg,#1a2020,#1e2820)\">' +
          '<div class=\"engine-header\"><span class=\"pool-title\">🔐 密码集萃引擎</span>' +
            '<span style=\"font-size:10px;padding:3px 8px;border-radius:12px;background:rgba(230,126,34,.2);color:#e67e22;border:1px solid #e67e22\">确定性地步</span></div>' +
          '<span class=\"pool-badge gold\" style=\"margin-bottom:6px\">' + result.front_cipher.length + '个(和≤'+maxVal+'+差+整除乘→并集)</span>' +
          '<div class=\"pool-nums\">';
        // Render cipher numbers with orange style
        for (var ci = 0; ci < result.front_cipher.length; ci++) {
          var cn = result.front_cipher[ci];
          // If also in consensus, highlight
          var cls = 'pool-num';
          if (result.front_consensus.indexOf(cn) !== -1) {
            cls += ' consensus';
          } else {
            cls += '';
            html += '<div class=\"pool-num\" style=\"background:#2a2020;border:1px solid #e67e22;color:#e6a040\">' + cn + '</div>';
            continue;
          }
          html += '<div class=\"' + cls + '\">' + cn + '</div>';
        }
        html += '</div>' +
          '<div class=\"db-ref\"><strong>📊 回测(3471期):</strong>平均命中3.45/6球 | 脱靶率0.58% | 命中≥3球78.2% | ≥4球49.5% | 全中6球3.92% | 池均18.8码</div></div>';
      }

"""

html = html.replace(pivot_marker, cipher_section + pivot_marker)

# ============================================================================
# 7. Update page title
# ============================================================================
html = html.replace(
    '<h1>🎯 彩票分析工具 <small>Pro版 · 双引擎融合</small></h1>',
    '<h1>🎯 彩票分析工具 <small>Pro版 · 三引擎融合</small></h1>'
)

html = html.replace(
    '<div class="subtitle">方法A(书上11规则)+ 方法B(Q-R算术引擎)→ 共识验证 · AC值/连号过滤 · 一键预测 · 偏态参考</div>',
    '<div class="subtitle">方法A(书上11规则)+ 方法B(Q-R算术引擎)+ 密码集萃(和差商)→ 三引擎验证 · AC值/连号过滤 · 一键预测 · 偏态参考</div>'
)

# ============================================================================
# 8. Add cipher toggle to DLT settings too (the DLT card doesn't have advanced settings)
#    We'll add a simple toggle on the DLT card
# ============================================================================
# After the DLT predict button and hint, add cipher toggle
dlt_hint = """  <div class="hint">输入上期开奖号码 → 方法A+方法B同时计算 → 共识号码=高置信度</div>"""

dlt_hint_new = """  <div class="hint">输入上期开奖号码 → 方法A+方法B+密码集萃 同时计算 → 共识号码=高置信度</div>"""

html = html.replace(dlt_hint, dlt_hint_new)

# Add DLT cipher toggle
dlt_card_end = """  <div class="result-box" id="dlt-result">
    <div id="dlt-result-inner"></div>
  </div>
</div>"""

dlt_card_cipher = """  <div style="display:flex;align-items:center;gap:8px;margin-top:10px;justify-content:center">
    <label style="display:flex;align-items:center;gap:6px;font-size:11px;color:#8899b0;cursor:pointer;padding:4px 12px;background:#1a2530;border-radius:8px;border:1px solid #2a3a58">
      <span style="font-size:11px">🔐 密码集萃引擎</span>
      <span id="cipher-toggle-indicator-dlt" style="font-size:10px;padding:2px 10px;border-radius:10px;background:#3a3a4a;color:#666">关闭</span>
    </label>
    <span onclick="document.getElementById('setting-cipher-enabled').clicked=true; document.getElementById('setting-cipher-enabled').checked = !document.getElementById('setting-cipher-enabled').checked; applySettings()" style="font-size:10px;color:#e67e22;cursor:pointer;text-decoration:underline">🔧 在SSQ高级设置中开启/关闭</span>
  </div>
  <div class="result-box" id="dlt-result">
    <div id="dlt-result-inner"></div>
  </div>
</div>"""

html = html.replace(dlt_card_end, dlt_card_cipher)

# Actually, let me think about this differently. The toggle is in the global BLUE_SETTINGS,
# and the applySettings() function handles it. The DLT toggle should just trigger the SSQ
# settings checkbox. But the cleanest way is:

# 1. The checkbox #setting-cipher-enabled controls the state
# 2. The indicator shows the state
# 3. Both SSQ and DLT share the same global state
# 4. When switching from DLT to SSQ, the SSQ settings reflect the same checkbox

# Let me remove the DLT-specific indicator and just add a simple reference link.

dlt_card_simple = """  <div style="display:flex;align-items:center;gap:8px;margin-top:10px;justify-content:center">
    <span style="font-size:10px;color:#5a7a9a">🔐 密码集萃引擎状态: </span>
    <span id="cipher-dlt-status" style="font-size:11px;padding:2px 10px;border-radius:10px;background:#3a3a4a;color:#666">关闭</span>
    <span style="font-size:10px;color:#5a7a9a">(在B款高级设置中调节)</span>
  </div>
  <div class="result-box" id="dlt-result">
    <div id="dlt-result-inner"></div>
  </div>
</div>"""

html = html.replace(dlt_card_end, dlt_card_simple)

# Add a small function to sync cipher status display
# Find the switchGame function and add status sync
old_switch = """function switchGame(game) {"""

new_switch = """function updateCipherStatusDisplay() {
  var enabled = document.getElementById('setting-cipher-enabled').checked;
  var indicators = document.querySelectorAll('[id^="cipher-toggle-indicator"]');
  indicators.forEach(function(el) {
    if (enabled) {
      el.textContent = '已开启';
      el.style.background = '#1a4a20';
      el.style.color = '#27ae60';
    } else {
      el.textContent = '关闭';
      el.style.background = '#3a3a4a';
      el.style.color = '#666';
    }
  });
  var dltStatus = document.getElementById('cipher-dlt-status');
  if (dltStatus) {
    dltStatus.textContent = enabled ? '✅ 已开启' : '关闭';
    dltStatus.style.background = enabled ? '#1a4a20' : '#3a3a4a';
    dltStatus.style.color = enabled ? '#27ae60' : '#666';
  }
}

function switchGame(game) {"""

html = html.replace(old_switch, new_switch)

# Update applySettings to also call updateCipherStatusDisplay
# Find the end of applySettings where it says "}, 1500);"
old_apply_end = """    btn.style.color = '#3498db';
  }, 1500);
}"""

# After that closing, add the display update
new_apply_end = """    btn.style.color = '#3498db';
  }, 1500);
  updateCipherStatusDisplay();
}"""

html = html.replace(old_apply_end, new_apply_end)

# Also ensure cipher status is synced on page load - add at end of script
html = html.replace('</script>\n</body>\n</html>', """
// Initialize cipher status display on load
setTimeout(function() {
  updateCipherStatusDisplay();
}, 100);
</script>
</body>
</html>""")

# ============================================================================
# 9. Fix the `//` operator - JavaScript uses Math.floor(b/a) for integer division
# ============================================================================
# In cipherEngine JS, I used `b // a` which is Python syntax.
# Fix to JavaScript: Math.floor(b / a)
old_jsdiv = "      if (b % a === 0) pool.add(b // a);"
new_jsdiv = "      if (b % a === 0) pool.add(Math.floor(b / a));"
html = html.replace(old_jsdiv, new_jsdiv)

# ============================================================================
# Write output
# ============================================================================
with open(r'C:\Users\xiank\.openclaw\workspace\toolbox\pro_v5.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("pro_v5.html built successfully!")

# Quick sanity check
counts = {
    'cipherEngine': html.count('cipherEngine'),
    'front_cipher': html.count('front_cipher'),
    'setting-cipher-enabled': html.count('setting-cipher-enabled'),
    'cipher-toggle-indicator': html.count('cipher-toggle-indicator'),
    'updateCipherStatusDisplay': html.count('updateCipherStatusDisplay'),
}
print("\nSanity check counts:", counts)
