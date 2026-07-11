#!/usr/bin/env python3
"""Build pro_v4.html with all three new features added."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\xiank\.openclaw\workspace\toolbox\pro.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ============================================================================
# 1. Enhanced consecutive functions (after getConsecutive)
# ============================================================================
old_consec = '''function getConsecutive(nums) {
  var sorted = nums.slice().sort(function(a,b){return a-b});
  var pairs = [];
  for (var i = 0; i < sorted.length - 1; i++) {
    if (sorted[i+1] - sorted[i] === 1) {
      pairs.push([sorted[i], sorted[i+1]]);
    }
  }
  return pairs;
}'''

new_consec = '''function getConsecutive(nums) {
  var sorted = nums.slice().sort(function(a,b){return a-b});
  var pairs = [];
  for (var i = 0; i < sorted.length - 1; i++) {
    if (sorted[i+1] - sorted[i] === 1) {
      pairs.push([sorted[i], sorted[i+1]]);
    }
  }
  return pairs;
}

// 奇连：依次相邻的奇数组合（如01,03,05）
function getConsecutiveOdd(nums) {
  var sorted = nums.slice().sort(function(a,b){return a-b});
  var odds = sorted.filter(function(n){return n%2===1;});
  var pairs = [];
  for (var i = 0; i < odds.length - 1; i++) {
    if (odds[i+1] - odds[i] === 2) {
      pairs.push([odds[i], odds[i+1]]);
    }
  }
  return pairs;
}

// 偶连：依次相邻的偶数组合（如02,04,06）
function getConsecutiveEven(nums) {
  var sorted = nums.slice().sort(function(a,b){return a-b});
  var evens = sorted.filter(function(n){return n%2===0;});
  var pairs = [];
  for (var i = 0; i < evens.length - 1; i++) {
    if (evens[i+1] - evens[i] === 2) {
      pairs.push([evens[i], evens[i+1]]);
    }
  }
  return pairs;
}

// 连号组数：独立的连号段落数量（如1,2,3,8,9 => 2组）
function getConsecutiveGroupCount(nums) {
  var sorted = nums.slice().sort(function(a,b){return a-b});
  if (sorted.length === 0) return 0;
  var groups = 1;
  for (var i = 0; i < sorted.length - 1; i++) {
    if (sorted[i+1] - sorted[i] !== 1) groups++;
  }
  return groups;
}

// 最大连号长度：一组连号中最多的数字个数（用于过滤）
function getMaxConsecutiveRun(nums) {
  var sorted = nums.slice().sort(function(a,b){return a-b});
  if (sorted.length === 0) return 0;
  var maxRun = 1, curRun = 1;
  for (var i = 0; i < sorted.length - 1; i++) {
    if (sorted[i+1] - sorted[i] === 1) {
      curRun++;
      if (curRun > maxRun) maxRun = curRun;
    } else {
      curRun = 1;
    }
  }
  return maxRun;
}'''

html = html.replace(old_consec, new_consec)

# ============================================================================
# 2. Update predict() return to include enhanced consecutive info
# ============================================================================
old_return = '''    ac_value: acValue(front),
    consecutive: getConsecutive(front),'''

new_return = '''    ac_value: acValue(front),
    consecutive: getConsecutive(front),
    consec_odd: getConsecutiveOdd(front),
    consec_even: getConsecutiveEven(front),
    consec_groups: getConsecutiveGroupCount(front),
    consec_max_run: getMaxConsecutiveRun(front),'''

html = html.replace(old_return, new_return)

# ============================================================================
# 3. Enhanced consecutive + AC value in stats display
# ============================================================================
old_stats_ac = '''      // Stats row
      var ac = typeof result.ac_value !== 'undefined' ? result.ac_value : '-';
      var cons = result.consecutive && result.consecutive.length > 0 ? result.consecutive.map(function(p) { return p[0] + '-' + p[1]; }) : [];

      html += '<div class="stats-row">' +
        '<div class="stat-item"><div class="stat-val">' + result.crash_pages + '/' + result.page_details.length + '</div><div class="stat-lbl">撞车页</div></div>' +
        '<div class="stat-item"><div class="stat-val">' + result.front_consensus.length + '</div><div class="stat-lbl">⭐共识</div></div>' +
        '<div class="stat-item"><div class="stat-val">' + result.front_a.length + '</div><div class="stat-lbl">📘方法A</div></div>' +
        '<div class="stat-item"><div class="stat-val">' + result.front_b.length + '</div><div class="stat-lbl">📗方法B</div></div>' +
        '</div>' +
        '<div class="stats-row">' +
        '<div class="stat-item"><div class="stat-val">' + ac + '</div><div class="stat-lbl">🧮 AC值</div></div>' +
        '<div class="stat-item"><div class="stat-val">' + (cons.length > 0 ? cons.length : 0) + '</div><div class="stat-lbl">🔗 连号数</div></div>' +
        '<div class="stat-item" style="flex:2"><div class="stat-val" style="font-size:13px;word-break:break-all">' + (cons.length > 0 ? cons.join(', ') : '无') + '</div><div class="stat-lbl">📊 连号详情</div></div>' +
        '</div>';'''

new_stats_ac = '''      // Stats row - with enhanced consecutive + AC value
      var ac = typeof result.ac_value !== 'undefined' ? result.ac_value : '-';
      var cons = result.consecutive && result.consecutive.length > 0 ? result.consecutive.map(function(p) { return p[0] + '-' + p[1]; }) : [];
      var consOdd = result.consec_odd && result.consec_odd.length > 0 ? result.consec_odd.map(function(p) { return p[0] + '-' + p[1]; }) : [];
      var consEven = result.consec_even && result.consec_even.length > 0 ? result.consec_even.map(function(p) { return p[0] + '-' + p[1]; }) : [];
      var acKill = isSSQ ? 3 : 2;

      html += '<div class="stats-row">' +
        '<div class="stat-item"><div class="stat-val">' + result.crash_pages + '/' + result.page_details.length + '</div><div class="stat-lbl">撞车页</div></div>' +
        '<div class="stat-item"><div class="stat-val">' + result.front_consensus.length + '</div><div class="stat-lbl">⭐共识</div></div>' +
        '<div class="stat-item"><div class="stat-val">' + result.front_a.length + '</div><div class="stat-lbl">📘方法A</div></div>' +
        '<div class="stat-item"><div class="stat-val">' + result.front_b.length + '</div><div class="stat-lbl">📗方法B</div></div>' +
        '</div>' +
        '<div class="stats-row">' +
        '<div class="stat-item"><div class="stat-val">' + ac + '</div><div class="stat-lbl" ' + (ac <= acKill ? 'style="color:#e74c3c"' : '') + '>🧮 AC值' + (ac <= acKill ? ' ⚠️极低' : '') + '</div></div>' +
        '<div class="stat-item"><div class="stat-val">' + (cons.length > 0 ? cons.length : 0) + '</div><div class="stat-lbl">🔗 连号数</div></div>' +
        '<div class="stat-item"><div class="stat-val">' + (consOdd.length > 0 ? consOdd.length : 0) + '</div><div class="stat-lbl">🔷 奇连</div></div>' +
        '<div class="stat-item"><div class="stat-val">' + (consEven.length > 0 ? consEven.length : 0) + '</div><div class="stat-lbl">🔶 偶连</div></div>' +
        '</div>' +
        '<div class="stats-row">' +
        '<div class="stat-item"><div class="stat-val">' + (typeof result.consec_groups !== 'undefined' ? result.consec_groups : '-') + '</div><div class="stat-lbl">📑 连号组数</div></div>' +
        '<div class="stat-item"><div class="stat-val">' + (typeof result.consec_max_run !== 'undefined' ? result.consec_max_run : '-') + '</div><div class="stat-lbl" ' + ((typeof result.consec_max_run !== 'undefined' && result.consec_max_run >= 5) ? 'style="color:#e74c3c"' : '') + '>📏 最长连号</div></div>' +
        '<div class="stat-item" style="flex:2"><div class="stat-val" style="font-size:12px;word-break:break-all">' + (cons.length > 0 ? cons.join(', ') : (consOdd.length > 0 || consEven.length > 0 ? '' : '无')) + ' ' +
          (consOdd.length > 0 ? '<span style="color:#5aa0d0">奇:' + consOdd.join(',') + '</span>' : '') + ' ' +
          (consEven.length > 0 ? '<span style="color:#e0a040">偶:' + consEven.join(',') + '</span>' : '') +
        '</div><div class="stat-lbl">📊 连号详情(普·奇·偶)</div></div>' +
        '</div>';'''

html = html.replace(old_stats_ac, new_stats_ac)

# ============================================================================
# 4. Auto-predict functions (inserted before 'function switchGame')
# ============================================================================
old_switch = '''function switchGame(game) {'''

new_switch = '''// ==================== AUTO PREDICT (从数据源自动获取最新期号) ====================
function getLastPeriodNumbers(type) {
  return loadLotteryData(type).then(function(data) {
    if (!data || data.length === 0) return null;
    var last = data[data.length - 1];
    return last;
  });
}

function autoPredictDLT() {
  var btn = document.getElementById('dlt-auto-btn');
  btn.textContent = '⏳ 加载中...';
  btn.disabled = true;

  getLastPeriodNumbers('dlt').then(function(last) {
    if (!last) {
      alert('数据文件不存在或为空。请确认 data/dlt.json 已部署。');
      btn.textContent = '🤖 自动获取最新期号并分析';
      btn.disabled = false;
      return;
    }

    // Fill front area inputs
    var fInputs = document.querySelectorAll('#dlt-front input');
    for (var i = 0; i < fInputs.length; i++) {
      fInputs[i].value = last.fronts[i];
    }

    // Fill back area inputs
    var bInputs = document.querySelectorAll('#dlt-back input');
    for (var i = 0; i < bInputs.length; i++) {
      bInputs[i].value = last.backs[i];
    }

    btn.textContent = '✅ ' + last.period + '期(' + last.date + ') 已加载,分析中...';

    // Auto trigger prediction
    setTimeout(function() {
      predictDLT();
      btn.textContent = '🤖 自动获取最新期号并分析';
      btn.disabled = false;
    }, 200);
  }).catch(function() {
    alert('数据加载失败');
    btn.textContent = '🤖 自动获取最新期号并分析';
    btn.disabled = false;
  });
}

function autoPredictSSQ() {
  var btn = document.getElementById('ssq-auto-btn');
  btn.textContent = '⏳ 加载中...';
  btn.disabled = true;

  getLastPeriodNumbers('ssq').then(function(last) {
    if (!last) {
      alert('数据文件不存在或为空。请确认 data/ssq.json 已部署。');
      btn.textContent = '🤖 自动获取最新期号并分析';
      btn.disabled = false;
      return;
    }

    // Fill reds
    var fInputs = document.querySelectorAll('#ssq-front input');
    for (var i = 0; i < fInputs.length; i++) {
      fInputs[i].value = last.reds[i];
    }

    // Fill blue
    document.getElementById('ssq-blue').value = last.blue;

    // Auto match blue history from data
    updateBlueHistoryFromData();

    btn.textContent = '✅ ' + last.period + '期(' + last.date + ') 已加载,蓝历史同步...';

    // Auto trigger prediction after a short delay for blue history to load
    setTimeout(function() {
      predictSSQ();
      btn.textContent = '🤖 自动获取最新期号并分析';
      btn.disabled = false;
    }, 300);
  }).catch(function() {
    alert('数据加载失败');
    btn.textContent = '🤖 自动获取最新期号并分析';
    btn.disabled = false;
  });
}

function switchGame(game) {'''

html = html.replace(old_switch, new_switch)

# ============================================================================
# 5. Add auto-predict buttons and AC filter settings to HTML
# ============================================================================
# DLT button: add after existing predict button
old_dlt_btn = '''  <button class="btn" onclick="predictDLT()">🔬 双引擎分析</button>'''
new_dlt_btn = '''  <div style="display:flex;gap:8px;margin-top:14px">
    <button class="btn" style="flex:1;margin:0" onclick="predictDLT()">🔬 双引擎分析</button>
    <button id="dlt-auto-btn" class="btn" style="flex:1;margin:0;background:#1a3050;color:#3498db;font-size:12px" onclick="autoPredictDLT()">🤖 自动获取最新期号</button>
  </div>'''
html = html.replace(old_dlt_btn, new_dlt_btn)

# SSQ button: add after existing predict button
old_ssq_btn = '''  <button class="btn" onclick="predictSSQ()">🔬 双引擎分析</button>'''
new_ssq_btn = '''  <div style="display:flex;gap:8px;margin-top:14px">
    <button class="btn" style="flex:1;margin:0" onclick="predictSSQ()">🔬 双引擎分析</button>
    <button id="ssq-auto-btn" class="btn" style="flex:1;margin:0;background:#1a3050;color:#3498db;font-size:12px" onclick="autoPredictSSQ()">🤖 自动获取最新期号</button>
  </div>'''
html = html.replace(old_ssq_btn, new_ssq_btn)

# ============================================================================
# 6. Add AC filter + consecutive filter to settings panel
# ============================================================================
old_filter_checkboxes = '''      <label style="font-size:11px">过滤策略(勾选=需同时满足)</label>
      <div style="display:flex;gap:10px;margin-top:4px;flex-wrap:wrap">
        <label style="display:flex;align-items:center;gap:4px;font-size:11px;color:#8899b0;cursor:pointer;margin:0">
          <input type="checkbox" id="setting-lonely" checked> 孤码
        </label>
        <label style="display:flex;align-items:center;gap:4px;font-size:11px;color:#8899b0;cursor:pointer;margin:0">
          <input type="checkbox" id="setting-mid" checked> 中码
        </label>
        <label style="display:flex;align-items:center;gap:4px;font-size:11px;color:#8899b0;cursor:pointer;margin:0">
          <input type="checkbox" id="setting-jump" checked> 跳码
        </label>
        <label style="display:flex;align-items:center;gap:4px;font-size:11px;color:#8899b0;cursor:pointer;margin:0">
          <input type="checkbox" id="setting-cold" checked> 冷码
        </label>
      </div>'''

new_filter_checkboxes = '''      <label style="font-size:11px">过滤策略(勾选=需同时满足)</label>
      <div style="display:flex;gap:10px;margin-top:4px;flex-wrap:wrap">
        <label style="display:flex;align-items:center;gap:4px;font-size:11px;color:#8899b0;cursor:pointer;margin:0">
          <input type="checkbox" id="setting-lonely" checked> 孤码
        </label>
        <label style="display:flex;align-items:center;gap:4px;font-size:11px;color:#8899b0;cursor:pointer;margin:0">
          <input type="checkbox" id="setting-mid" checked> 中码
        </label>
        <label style="display:flex;align-items:center;gap:4px;font-size:11px;color:#8899b0;cursor:pointer;margin:0">
          <input type="checkbox" id="setting-jump" checked> 跳码
        </label>
        <label style="display:flex;align-items:center;gap:4px;font-size:11px;color:#8899b0;cursor:pointer;margin:0">
          <input type="checkbox" id="setting-cold" checked> 冷码
        </label>
      </div>

      <hr style="border:0;border-top:1px solid #1e2a40;margin:10px 0">
      <div style="font-size:12px;color:#f0c040;margin-bottom:6px">🎯 号码范围过滤(淘汰极罕见组合)</div>

      <label style="font-size:11px">AC值过滤(淘汰极低AC组合)</label>
      <div style="display:flex;align-items:center;gap:10px;margin-top:4px">
        <label style="display:flex;align-items:center;gap:4px;font-size:11px;color:#8899b0;cursor:pointer;margin:0">
          <input type="checkbox" id="setting-ac-kill" checked> 淘汰AC≤
        </label>
        <span id="ac-kill-label" style="font-size:13px;color:#f0c040;min-width:40px">(SSQ≤3,DLT≤2)</span>
      </div>

      <label style="font-size:11px">连号限制</label>
      <div style="display:flex;align-items:center;gap:10px;margin-top:4px;flex-wrap:wrap">
        <label style="display:flex;align-items:center;gap:4px;font-size:11px;color:#8899b0;cursor:pointer;margin:0">
          <input type="checkbox" id="setting-consec-kill" checked> 淘汰最长连号≥
        </label>
        <input type="range" id="setting-consec-max" min="4" max="7" value="5" oninput="document.getElementById('consec-max-val').textContent=this.value" style="flex:0.5;accent-color:#e74c3c">
        <span id="consec-max-val" style="font-size:14px;color:#e74c3c;min-width:20px">5</span>
      </div>'''

html = html.replace(old_filter_checkboxes, new_filter_checkboxes)

# ============================================================================
# 7. Update BLUE_SETTINGS to include new filter config
# ============================================================================
old_settings_obj = '''var BLUE_SETTINGS = {
  coldHotWindow: 11, hotThreshold: 3, warmThreshold: 2,
  filterLonely: true, filterMid: true, filterJump: true, filterCold: true
};'''

new_settings_obj = '''var BLUE_SETTINGS = {
  coldHotWindow: 11, hotThreshold: 3, warmThreshold: 2,
  filterLonely: true, filterMid: true, filterJump: true, filterCold: true,
  filterAcKill: true,  // 淘汰极低AC值
  filterConsecKill: true,  // 淘汰超长连号
  consecMaxRun: 5  // 最长连号上限
};'''

html = html.replace(old_settings_obj, new_settings_obj)

# ============================================================================
# 8. Update applySettings to include new filters
# ============================================================================
old_apply = '''function applySettings() {
  BLUE_SETTINGS.coldHotWindow = parseInt(document.getElementById('setting-window').value) || 11;
  BLUE_SETTINGS.hotThreshold = parseInt(document.getElementById('setting-hot').value) || 3;
  BLUE_SETTINGS.warmThreshold = parseInt(document.getElementById('setting-warm').value) || 2;
  BLUE_SETTINGS.filterLonely = document.getElementById('setting-lonely').checked;
  BLUE_SETTINGS.filterMid = document.getElementById('setting-mid').checked;
  BLUE_SETTINGS.filterJump = document.getElementById('setting-jump').checked;
  BLUE_SETTINGS.filterCold = document.getElementById('setting-cold').checked;

  var btn = document.getElementById('save-settings');
  btn.textContent = '✅ 已保存';
  btn.style.background = '#1a3a20';
  btn.style.color = '#27ae60';
  setTimeout(function() {
    btn.textContent = '设置';
    btn.style.background = '#1a3050';
    btn.style.color = '#3498db';
  }, 1500);
}'''

new_apply = '''function applySettings() {
  BLUE_SETTINGS.coldHotWindow = parseInt(document.getElementById('setting-window').value) || 11;
  BLUE_SETTINGS.hotThreshold = parseInt(document.getElementById('setting-hot').value) || 3;
  BLUE_SETTINGS.warmThreshold = parseInt(document.getElementById('setting-warm').value) || 2;
  BLUE_SETTINGS.filterLonely = document.getElementById('setting-lonely').checked;
  BLUE_SETTINGS.filterMid = document.getElementById('setting-mid').checked;
  BLUE_SETTINGS.filterJump = document.getElementById('setting-jump').checked;
  BLUE_SETTINGS.filterCold = document.getElementById('setting-cold').checked;
  BLUE_SETTINGS.filterAcKill = document.getElementById('setting-ac-kill').checked;
  BLUE_SETTINGS.filterConsecKill = document.getElementById('setting-consec-kill').checked;
  BLUE_SETTINGS.consecMaxRun = parseInt(document.getElementById('setting-consec-max').value) || 5;

  var btn = document.getElementById('save-settings');
  btn.textContent = '✅ 已保存';
  btn.style.background = '#1a3a20';
  btn.style.color = '#27ae60';
  setTimeout(function() {
    btn.textContent = '设置';
    btn.style.background = '#1a3050';
    btn.style.color = '#3498db';
  }, 1500);
}'''

html = html.replace(old_apply, new_apply)

# ============================================================================
# 9. Update genCombos to pass isSSQ and apply AC/Consec filtering
# ============================================================================
# Need to change genCombos to accept an isSSQ param and filter combos
old_gen = '''function genCombos(pool, pool2, cnt, size1, size2) {
  if (pool.length < size1) return [];
  var combos = [];
  var seeds = [42, 123, 777, 999, 555];
  for (var si = 0; si < Math.min(cnt, seeds.length); si++) {
    var s = pool.slice();
    for (var i = s.length - 1; i > 0; i--) {
      var j = Math.floor((seeds[si] * (i + 1) + si * 13) % (i + 1));
      var tmp = s[i]; s[i] = s[j]; s[j] = tmp;
    }
    var f = s.slice(0, size1).sort(function(a, b) { return a - b; });
    var sc = pool2.slice();
    for (var k = sc.length - 1; k > 0; k--) {
      var j2 = Math.floor((seeds[si] * (k + 1) + si * 37) % (k + 1));
      var tmp2 = sc[k]; sc[k] = sc[j2]; sc[j2] = tmp2;
    }
    var bk = sc.slice(0, size2).sort(function(a, b) { return a - b; });
    combos.push([f, bk]);
  }
  return combos;
}'''

new_gen = '''function genCombos(pool, pool2, cnt, size1, size2, isSSQ) {
  if (pool.length < size1) return [];
  var settings = (typeof BLUE_SETTINGS !== 'undefined') ? BLUE_SETTINGS : { filterAcKill:true, filterConsecKill:true, consecMaxRun:5 };
  var acKill = isSSQ ? 3 : 2;

  var combos = [];
  var seeds = [42, 123, 777, 999, 555];

  // Shuffle once and take sequential chunks to get more variety
  var shuffled = pool.slice();
  for (var i = shuffled.length - 1; i > 0; i--) {
    var j = Math.floor(Math.random() * (i + 1));
    var tmp = shuffled[i]; shuffled[i] = shuffled[j]; shuffled[j] = tmp;
  }

  for (var si = 0; si < Math.min(cnt, seeds.length); si++) {
    // Try multiple offsets until we find a valid combo or exhaust
    var maxTries = 100;
    var found = false;
    for (var attempt = 0; attempt < maxTries && !found; attempt++) {
      var offset = (si * 7 + attempt * 17) % Math.max(1, shuffled.length - size1);
      var f = shuffled.slice(offset, offset + size1).sort(function(a, b) { return a - b; });

      // AC value filter
      if (settings.filterAcKill && acValue(f) <= acKill) continue;

      // Consecutive run filter
      if (settings.filterConsecKill && getMaxConsecutiveRun(f) >= settings.consecMaxRun) continue;

      // Found a valid front combo
      var sc = pool2.slice();
      for (var k = sc.length - 1; k > 0; k--) {
        var j2 = Math.floor((seeds[si] * (k + 1) + si * 37) % (k + 1));
        var tmp2 = sc[k]; sc[k] = sc[j2]; sc[j2] = tmp2;
      }
      var bk = sc.slice(0, size2).sort(function(a, b) { return a - b; });
      combos.push([f, bk]);
      found = true;
    }
    // If all attempts failed, push a plain combo without filtering
    if (!found) {
      var offset = si * 5 % Math.max(1, shuffled.length - size1);
      var f = shuffled.slice(offset, offset + size1).sort(function(a, b) { return a - b; });
      var sc = pool2.slice();
      for (var k = sc.length - 1; k > 0; k--) {
        var j2 = Math.floor((seeds[si] * (k + 1) + si * 37) % (k + 1));
        var tmp2 = sc[k]; sc[k] = sc[j2]; sc[j2] = tmp2;
      }
      var bk = sc.slice(0, size2).sort(function(a, b) { return a - b; });
      combos.push([f, bk]);
    }
  }
  return combos;
}'''

html = html.replace(old_gen, new_gen)

# ============================================================================
# 10. Update renderResult: pass isSSQ to genCombos calls
# ============================================================================
# Find genCombos calls in renderResult
html = html.replace(
    "    html += renderCombos(result, frontMax, backMax, isSSQ);",
    "    html += renderCombos(result, frontMax, backMax, isSSQ, isSSQ);"
)

# Update renderCombos to pass isSSQ
old_rc = '''function renderCombos(result, frontMax, backMax, isSSQ) {'''
new_rc = '''function renderCombos(result, frontMax, backMax, isSSQ, acFlag) {'''
html = html.replace(old_rc, new_rc)

# Update genCombos call inside renderCombos
html = html.replace(
    "    var combos = genCombos(comboPool, backPool, 5, size1, size2);",
    "    var combos = genCombos(comboPool, backPool, 5, size1, size2, acFlag);"
)

# ============================================================================
# Write result
# ============================================================================
with open(r'C:\Users\xiank\.openclaw\workspace\toolbox\pro.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f'Written: {len(html)} bytes')
print('Done!')
