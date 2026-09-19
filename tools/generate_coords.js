#!/usr/bin/env node
/**
 * generate_coords.js - Generate 2D molecular coordinates using RDKit.js (WASM)
 * SINGLE SOURCE for molecular coordinate generation.
 * Usage: node generate_coords.js --smiles "CCO" --name ethanol
 *        node generate_coords.js --batch molecules.json
 *
 * molecules.json format:
 *   { "ethanol": "CCO", "benzene": "c1ccccc1" }
 *
 * Output: molecule_outputs/<name>.json with atoms (x,y,z,element) and bonds (atom1,atom2,bondType)
 */
const fs = require('fs');
const path = require('path');
const vm = require('vm');

// Paths
const SCRIPT_DIR = __dirname;
const SKILL_ROOT = path.resolve(SCRIPT_DIR, '..');
const RDKIT_JS = path.join(SKILL_ROOT, 'rdkit', 'RDKit_minimal.js');
const RDKIT_WASM = path.join(SKILL_ROOT, 'rdkit', 'RDKit_minimal.wasm');
const OUTPUT_DIR = path.join(SKILL_ROOT, 'molecule_outputs');

// Parse CLI args
function parseArgs() {
  const args = process.argv.slice(2);
  const opts = { smiles: null, name: null, batch: null, outputDir: OUTPUT_DIR, svg: false };
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--smiles') opts.smiles = args[++i];
    else if (args[i] === '--name') opts.name = args[++i];
    else if (args[i] === '--batch') opts.batch = args[++i];
    else if (args[i] === '--output') opts.outputDir = args[++i];
    else if (args[i] === '--svg') opts.svg = true;
    else if (args[i] === '--help' || args[i] === '-h') {
      console.log('Usage: node generate_coords.js --smiles "CCO" --name ethanol');
      console.log('       node generate_coords.js --batch molecules.json [--svg]');
      process.exit(0);
    }
  }
  return opts;
}

// Initialize RDKit in a VM sandbox
async function initRDKit() {
  const wasmBuffer = fs.readFileSync(RDKIT_WASM);
  const jsCode = fs.readFileSync(RDKIT_JS, 'utf8');

  const sandbox = {
    window: {},
    self: {},
    location: { href: 'http://localhost/' },
    navigator: { userAgent: 'node' },
    fetch: (url) => Promise.resolve({
      ok: true,
      arrayBuffer: () => Promise.resolve(wasmBuffer.buffer.slice(wasmBuffer.byteOffset, wasmBuffer.byteOffset + wasmBuffer.byteLength)),
    }),
    console: console,
    setTimeout: setTimeout,
  };
  sandbox.global = sandbox;
  vm.createContext(sandbox);
  vm.runInContext(jsCode, sandbox);

  const RDKit = await sandbox.initRDKitModule();
  return RDKit;
}

// Parse MOL V2000 block into atoms and bonds
function parseMolBlock(molblock) {
  const lines = molblock.split('\n');
  const countsLine = lines[3];
  const numAtoms = parseInt(countsLine.substring(0, 3).trim(), 10);
  const numBonds = parseInt(countsLine.substring(3, 6).trim(), 10);

  const atoms = [];
  for (let i = 0; i < numAtoms; i++) {
    const line = lines[4 + i];
    const x = parseFloat(line.substring(0, 10).trim());
    const y = parseFloat(line.substring(10, 20).trim());
    const z = parseFloat(line.substring(20, 30).trim());
    const element = line.substring(31, 34).trim();
    atoms.push({ index: i + 1, x, y, z, element });
  }

  const bonds = [];
  for (let i = 0; i < numBonds; i++) {
    const line = lines[4 + numAtoms + i];
    const atom1 = parseInt(line.substring(0, 3).trim(), 10);
    const atom2 = parseInt(line.substring(3, 6).trim(), 10);
    const bondType = parseInt(line.substring(6, 9).trim(), 10);
    bonds.push({ atom1, atom2, bondType });
  }

  return { atoms, bonds, numAtoms, numBonds };
}

// Generate coordinates for a single molecule
function generateMolecule(RDKit, smiles, name) {
  const mol = RDKit.get_mol(smiles);
  if (!mol.is_valid()) {
    console.error(`  [ERROR] ${name}: invalid SMILES "${smiles}"`);
    return null;
  }

  const molblock = mol.get_molblock();
  const parsed = parseMolBlock(molblock);
  const svg = mol.get_svg();

  const result = {
    name,
    smiles,
    numAtoms: parsed.numAtoms,
    numBonds: parsed.numBonds,
    atoms: parsed.atoms,
    bonds: parsed.bonds,
  };

  mol.delete();
  return { result, svg };
}

// Main
async function main() {
  const opts = parseArgs();

  if (!fs.existsSync(opts.outputDir)) {
    fs.mkdirSync(opts.outputDir, { recursive: true });
  }

  console.log('Initializing RDKit.js (WASM)...');
  const RDKit = await initRDKit();
  console.log('RDKit ready.');

  let molecules = {};
  if (opts.batch) {
    const batchData = JSON.parse(fs.readFileSync(opts.batch, 'utf8'));
    molecules = batchData;
    console.log(`Batch mode: ${Object.keys(molecules).length} molecules from ${opts.batch}`);
  } else if (opts.smiles) {
    const name = opts.name || opts.smiles.replace(/[^a-zA-Z0-9]/g, '_');
    molecules = { [name]: opts.smiles };
  } else {
    console.error('Error: specify --smiles or --batch');
    process.exit(1);
  }

  const summary = {};
  let success = 0;

  for (const [name, smiles] of Object.entries(molecules)) {
    const gen = generateMolecule(RDKit, smiles, name);
    if (!gen) continue;

    const jsonPath = path.join(opts.outputDir, `${name}.json`);
    fs.writeFileSync(jsonPath, JSON.stringify(gen.result, null, 2));

    if (opts.svg) {
      const svgPath = path.join(opts.outputDir, `${name}.svg`);
      fs.writeFileSync(svgPath, gen.svg);
    }

    summary[name] = { atoms: gen.result.numAtoms, bonds: gen.result.numBonds };
    success++;
    console.log(`  [OK] ${name}: ${gen.result.numAtoms} atoms, ${gen.result.numBonds} bonds`);
  }

  fs.writeFileSync(path.join(opts.outputDir, '_summary.json'), JSON.stringify(summary, null, 2));
  console.log(`\n${success}/${Object.keys(molecules).length} molecules generated.`);
  console.log(`Output: ${opts.outputDir}`);
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});