// Verifica cálculos, carga y navegación con DOM/Chart simulados; no sustituye un navegador.
// Ejecutar: node tools/verificar_html.js [raíz_del_proyecto]
'use strict';
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const { webcrypto } = require('node:crypto');
const root = path.resolve(process.argv[2] || path.join(__dirname, '..'));
function environment(html) {
    const nodes = new Map();
    const events = new Map();
    const alerts = [];
    const charts = [];
    function node(id) {
        if (!nodes.has(id)) nodes.set(id, {
            id, innerText: '', textContent: '', title: '',
            classList: { values: new Set(), add(x) { this.values.add(x); },
                remove(x) { this.values.delete(x); }, toggle(x, value) {
                    if (value === undefined) value = !this.values.has(x);
                    if (value) this.add(x); else this.remove(x);
                } },
            addEventListener(name, fn) { events.set(id + ':' + name, fn); },
            getContext() { return { id }; }
        });
        return nodes.get(id);
    }
    const ids = [...html.matchAll(/\bid="([^"]+)"/g)].map(x => x[1]);
    assert.equal(new Set(ids).size, ids.length, 'IDs duplicados');
    ids.forEach(node);
    const slideCount = [...html.matchAll(/class="[^"]*\bslide\b[^"]*"/g)].length;
    const slides = Array.from({ length: slideCount }, (_, i) => node('slide_' + i));
    const document = {
        getElementById(id) { assert(nodes.has(id), 'Elemento inexistente: ' + id); return node(id); },
        querySelectorAll(selector) { assert.equal(selector, '.slide'); return slides; },
        addEventListener(name, fn) { events.set('document:' + name, fn); }
    };
    const context = vm.createContext({ document, console, TextEncoder, crypto: webcrypto,
        alert(message) { alerts.push(message); },
        Chart: class {
            constructor(ctx, spec) { this.id = ctx.id; this.spec = spec; this.destroyed = false; charts.push(this); }
            destroy() { this.destroyed = true; }
        }
    });
    const scripts = [...html.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/gi)].map(x => x[1]).filter(x => x.trim());
    scripts.forEach(script => vm.runInContext(script, context));
    return { context, nodes, events, alerts, charts, slides };
}
(async () => {
    const report = environment(fs.readFileSync(path.join(root, 'reportes_analisis_dataset_principal.html'), 'utf8'));
    const csv = fs.readFileSync(path.join(root, 'dataset/ai_student_impact_dataset (1).csv'), 'utf8');
    const parsed = report.context.parseCSV(csv);
    assert.equal(parsed.data.length, 50000);
    assert.equal(parsed.headers.length, 16);
    const counts = { Low: 0, Medium: 0, High: 0 };
    parsed.data.forEach(row => counts[row.Burnout_Risk_Level]++);
    assert.deepEqual(counts, { Low: 16369, Medium: 21144, High: 12487 });
    const changed = report.events.get('csvFileInput:change');
    await changed({ target: { files: [{ name: 'ai_student_impact_dataset (1).csv', text: async () => csv }] } });
    assert.equal(report.alerts.length, 0);
    assert.equal(report.nodes.get('kpiHigh').innerText, '24.974 %');
    assert.equal(Number(report.nodes.get('totalStudents').innerText.replace(/\D/g, '')), 50000);
    assert.equal(report.nodes.get('avgAiHours').innerText, '8.4');
    assert.equal(report.nodes.get('avgTradHours').innerText, '11.2');
    assert.equal(report.nodes.get('avgAnxiety').innerText, '4.3');
    assert.equal(report.charts.length, 4);
    report.charts.forEach(chart => chart.spec.data.datasets.forEach(dataset => assert(dataset.data.every(Number.isFinite))));
    assert.equal(report.charts.find(c => c.id === 'yearChart').spec.data.datasets[0].data.reduce((a, b) => a + b), 50000);
    assert.equal(report.charts.find(c => c.id === 'policyChart').spec.data.datasets[0].data.reduce((a, b) => a + b), 50000);
    await changed({ target: { files: [{ name: 'CRLF.csv', text: async () => csv.replace(/\n/g, '\r\n') }] } });
    assert.equal(report.alerts.length, 0);
    assert(report.charts.slice(0, 4).every(chart => chart.destroyed));
    await changed({ target: { files: [{ name: 'alterado.csv', text: async () => csv.replace('Low', 'High') }] } });
    assert.equal(report.alerts.length, 1);
    assert(report.nodes.get('dashboardContent').classList.values.has('hidden'));
    assert.throws(() => report.context.parseCSV(''));
    assert.throws(() => report.context.parseCSV(csv.split('\n').slice(0, -2).join('\n')));
    assert.throws(() => report.context.parseCSV(csv.replace('Student_ID', 'ID')));
    const presentation = environment(fs.readFileSync(path.join(root, 'presentacion_eduanalytics.html'), 'utf8'));
    assert(presentation.slides.length > 1);
    presentation.context.showSlide(0);
    assert.equal(presentation.nodes.get('counter').textContent, `1 / ${presentation.slides.length}`);
    presentation.context.nextSlide();
    assert.equal(presentation.nodes.get('counter').textContent, `2 / ${presentation.slides.length}`);
    presentation.context.prevSlide();
    assert.equal(presentation.nodes.get('counter').textContent, `1 / ${presentation.slides.length}`);
    presentation.events.get('document:keydown')({ key: 'ArrowRight' });
    assert.equal(presentation.nodes.get('counter').textContent, `2 / ${presentation.slides.length}`);
    presentation.context.showSlide(-1);
    assert.equal(presentation.nodes.get('counter').textContent, `${presentation.slides.length} / ${presentation.slides.length}`);
    console.log(JSON.stringify({ Node: process.version, report: 'PASS', csv_rows: 50000, csv_columns: 16,
        classes: counts, high_kpi_percent: '24.974', charts_finite: 4, upload_lf_crlf: 'PASS',
        altered_file_rejected: 'PASS', presentation_navigation: 'PASS', slides: presentation.slides.length,
        browser_rendering: 'PENDING: prueba con DOM y Chart simulados, sin navegador.' }, null, 2));
})().catch(error => { console.error(error); process.exitCode = 1; });
