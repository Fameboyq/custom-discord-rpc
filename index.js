/**
 * Custom Discord Rich Presence (RPC) - Universal Multi-Language Engine
 * Author: Fameboyq (https://github.com/Fameboyq)
 * License: MIT
 */

const fs = require('fs');
const path = require('path');
const RPC = require('discord-rpc');

const CONFIG_PATH = path.join(__dirname, 'config.json');

function loadConfig() {
    try {
        if (fs.existsSync(CONFIG_PATH)) {
            const raw = fs.readFileSync(CONFIG_PATH, 'utf8');
            return JSON.parse(raw);
        }
    } catch (err) {
        console.error('[RPC] Error reading config.json:', err.message);
    }
    return {
        client_id: '1440730997460172810',
        enabled: true,
        language: 'en',
        interval_seconds: 6,
        buttons: []
    };
}

let config = loadConfig();
let client = null;
let isConnected = false;
let isConnecting = false;
let startTime = Date.now();
let currentFrameIndex = 0;

function log(msg) {
    const time = new Date().toLocaleTimeString();
    console.log(`[${time}] ${msg}`);
}

function getFrames() {
    config = loadConfig();
    const lang = (config.language || 'en').toLowerCase();
    const presets = config.presets || {};
    return presets[lang] || presets['en'] || [];
}

function updatePresence() {
    if (!client || !isConnected) return;
    if (config.enabled === false) {
        client.clearActivity().catch(() => {});
        return;
    }

    const frames = getFrames();
    if (!frames || frames.length === 0) return;

    const frame = frames[currentFrameIndex % frames.length];
    currentFrameIndex = (currentFrameIndex + 1) % frames.length;

    const activity = {
        details: (frame.details || '').slice(0, 128),
        state: (frame.state || '').slice(0, 128),
        startTimestamp: startTime,
        largeImageKey: frame.large_image || 'antigravity_logo',
        largeImageText: (frame.large_text || '').slice(0, 128),
        smallImageKey: frame.small_image || 'robot',
        smallImageText: (frame.small_text || '').slice(0, 128),
        instance: false
    };

    if (Array.isArray(config.buttons) && config.buttons.length > 0) {
        const validButtons = config.buttons
            .filter(b => b.label && b.url)
            .slice(0, 2)
            .map(b => ({
                label: b.label.slice(0, 32),
                url: b.url
            }));

        if (validButtons.length > 0) {
            activity.buttons = validButtons;
        }
    }

    client.setActivity(activity).catch(err => {
        log(`Failed to set activity: ${err.message}`);
    });
}

function connect() {
    if (isConnected || isConnecting) return;
    isConnecting = true;

    config = loadConfig();
    const clientId = config.client_id || '1440730997460172810';

    try {
        client = new RPC.Client({ transport: 'ipc' });

        client.on('ready', () => {
            isConnected = true;
            isConnecting = false;
            startTime = Date.now();
            const lang = config.language || 'en';
            if (lang === 'ru') {
                log(`⚡ Discord RPC успешно запущен! Клиент ID: ${clientId}`);
                log(`Язык: Русский | Интервал анимации: ${config.interval_seconds || 6} сек.`);
            } else {
                log(`⚡ Discord RPC connected successfully! Client ID: ${clientId}`);
                log(`Language: English | Rotation Interval: ${config.interval_seconds || 6}s`);
            }
            updatePresence();
        });

        client.on('disconnected', () => {
            isConnected = false;
            isConnecting = false;
            client = null;
            log('Discord RPC disconnected. Retrying in 5 seconds...');
            setTimeout(connect, 5000);
        });

        client.login({ clientId }).catch(() => {
            isConnected = false;
            isConnecting = false;
            client = null;
            setTimeout(connect, 5000);
        });
    } catch (e) {
        isConnected = false;
        isConnecting = false;
        client = null;
        setTimeout(connect, 5000);
    }
}

// Initial connection
connect();

// Interval loop
const intervalMs = Math.max(3000, (config.interval_seconds || 6) * 1000);
setInterval(() => {
    if (isConnected) {
        updatePresence();
    } else {
        connect();
    }
}, intervalMs);
