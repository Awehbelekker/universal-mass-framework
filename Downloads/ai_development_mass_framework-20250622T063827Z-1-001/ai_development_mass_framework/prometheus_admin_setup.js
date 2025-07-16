/**
 * PROMETHEUS Admin Account Setup Script
 * Creates the default admin account and fixes Firebase configuration
 */

// Default admin credentials
const ADMIN_CREDENTIALS = {
    email: 'admin@prometheus-neural-forge.com',
    password: 'PrometheusAdmin2025!',
    displayName: 'PROMETHEUS Administrator',
    role: 'admin',
    permissions: ['all'],
    accessLevel: 'admin'
};

console.log('🔥 PROMETHEUS Admin Setup Initializing...');

// Initialize Firebase if not already done
if (typeof firebase === 'undefined') {
    console.log('Firebase not loaded, please ensure Firebase SDK is included');
} else {
    console.log('✅ Firebase SDK detected');
    
    // Firebase configuration for ai-mass-trading
    const firebaseConfig = {
        apiKey: "AIzaSyBqHKr0tQe_8x4n3zF8R7HJmjh9cZ3XyXY",
        authDomain: "ai-mass-trading.firebaseapp.com",
        projectId: "ai-mass-trading",
        storageBucket: "ai-mass-trading.appspot.com",
        messagingSenderId: "1046048153364",
        appId: "1:1046048153364:web:abc123def456789"
    };
    
    // Initialize Firebase if not already initialized
    if (!firebase.apps.length) {
        firebase.initializeApp(firebaseConfig);
    }
    
    const auth = firebase.auth();
    const db = firebase.firestore();
    
    // Function to create admin account
    async function createAdminAccount() {
        try {
            console.log('👤 Creating admin account...');
            
            // Create admin user in Firebase Auth
            const userCredential = await auth.createUserWithEmailAndPassword(
                ADMIN_CREDENTIALS.email, 
                ADMIN_CREDENTIALS.password
            );
            
            const user = userCredential.user;
            
            // Update display name
            await user.updateProfile({
                displayName: ADMIN_CREDENTIALS.displayName
            });
            
            console.log('✅ Admin user created in Firebase Auth:', user.uid);
            
            // Create admin document in Firestore
            await db.collection('allowed_users').doc(ADMIN_CREDENTIALS.email).set({
                email: ADMIN_CREDENTIALS.email,
                displayName: ADMIN_CREDENTIALS.displayName,
                role: ADMIN_CREDENTIALS.role,
                permissions: ADMIN_CREDENTIALS.permissions,
                accessLevel: ADMIN_CREDENTIALS.accessLevel,
                uid: user.uid,
                createdAt: new Date().toISOString(),
                lastLogin: new Date().toISOString(),
                status: 'active'
            });
            
            console.log('✅ Admin document created in Firestore');
            
            // Create admin user profile
            await db.collection('users').doc(user.uid).set({
                email: ADMIN_CREDENTIALS.email,
                displayName: ADMIN_CREDENTIALS.displayName,
                role: ADMIN_CREDENTIALS.role,
                permissions: ADMIN_CREDENTIALS.permissions,
                accessLevel: ADMIN_CREDENTIALS.accessLevel,
                tradingLevel: 'real',
                accountBalance: 100000,
                portfolioValue: 100000,
                totalPnL: 0,
                riskLevel: 'medium',
                realMoneyEnabled: true,
                status: 'active',
                createdAt: new Date().toISOString(),
                lastLogin: new Date().toISOString()
            });
            
            console.log('✅ Admin user profile created');
            
            // Log success
            console.log('🎉 Admin account setup complete!');
            console.log('📧 Email:', ADMIN_CREDENTIALS.email);
            console.log('🔑 Password:', ADMIN_CREDENTIALS.password);
            console.log('🔗 Admin Portal:', 'https://ai-mass-trading.web.app/admin.html');
            
            return true;
            
        } catch (error) {
            if (error.code === 'auth/email-already-in-use') {
                console.log('👤 Admin account already exists, updating permissions...');
                
                try {
                    // Sign in to get user
                    const signInResult = await auth.signInWithEmailAndPassword(
                        ADMIN_CREDENTIALS.email, 
                        ADMIN_CREDENTIALS.password
                    );
                    
                    const user = signInResult.user;
                    
                    // Update Firestore documents
                    await db.collection('allowed_users').doc(ADMIN_CREDENTIALS.email).set({
                        email: ADMIN_CREDENTIALS.email,
                        displayName: ADMIN_CREDENTIALS.displayName,
                        role: ADMIN_CREDENTIALS.role,
                        permissions: ADMIN_CREDENTIALS.permissions,
                        accessLevel: ADMIN_CREDENTIALS.accessLevel,
                        uid: user.uid,
                        updatedAt: new Date().toISOString(),
                        lastLogin: new Date().toISOString(),
                        status: 'active'
                    }, { merge: true });
                    
                    await db.collection('users').doc(user.uid).set({
                        email: ADMIN_CREDENTIALS.email,
                        displayName: ADMIN_CREDENTIALS.displayName,
                        role: ADMIN_CREDENTIALS.role,
                        permissions: ADMIN_CREDENTIALS.permissions,
                        accessLevel: ADMIN_CREDENTIALS.accessLevel,
                        tradingLevel: 'real',
                        realMoneyEnabled: true,
                        updatedAt: new Date().toISOString(),
                        lastLogin: new Date().toISOString()
                    }, { merge: true });
                    
                    console.log('✅ Admin account updated successfully');
                    return true;
                    
                } catch (updateError) {
                    console.error('❌ Failed to update admin account:', updateError);
                    return false;
                }
            } else {
                console.error('❌ Failed to create admin account:', error);
                return false;
            }
        }
    }
    
    // Function to create demo users for testing
    async function createDemoUsers() {
        const demoUsers = [
            {
                email: 'demo1@prometheus-trading.com',
                password: 'Demo2025!',
                displayName: 'Demo Trader 1',
                tradingLevel: 'paper'
            },
            {
                email: 'demo2@prometheus-trading.com',
                password: 'Demo2025!',
                displayName: 'Demo Trader 2',
                tradingLevel: 'paper'
            },
            {
                email: 'live1@prometheus-trading.com',
                password: 'Live2025!',
                displayName: 'Live Trader 1',
                tradingLevel: 'live'
            },
            {
                email: 'live2@prometheus-trading.com',
                password: 'Live2025!',
                displayName: 'Live Trader 2',
                tradingLevel: 'live'
            }
        ];
        
        console.log('👥 Creating demo users...');
        
        for (const demoUser of demoUsers) {
            try {
                const userCredential = await auth.createUserWithEmailAndPassword(
                    demoUser.email, 
                    demoUser.password
                );
                
                const user = userCredential.user;
                
                await user.updateProfile({
                    displayName: demoUser.displayName
                });
                
                // Create user profile
                await db.collection('users').doc(user.uid).set({
                    email: demoUser.email,
                    displayName: demoUser.displayName,
                    role: 'user',
                    tradingLevel: demoUser.tradingLevel,
                    accountBalance: demoUser.tradingLevel === 'live' ? 100000 : 50000,
                    portfolioValue: demoUser.tradingLevel === 'live' ? 100000 : 50000,
                    totalPnL: 0,
                    riskLevel: 'medium',
                    status: 'active',
                    createdAt: new Date().toISOString()
                });
                
                // Add to allowed users
                await db.collection('allowed_users').doc(demoUser.email).set({
                    email: demoUser.email,
                    displayName: demoUser.displayName,
                    role: 'user',
                    accessLevel: 'user',
                    uid: user.uid,
                    createdAt: new Date().toISOString(),
                    status: 'active'
                });
                
                console.log(`✅ Created demo user: ${demoUser.email}`);
                
            } catch (error) {
                if (error.code === 'auth/email-already-in-use') {
                    console.log(`👤 Demo user already exists: ${demoUser.email}`);
                } else {
                    console.error(`❌ Failed to create demo user ${demoUser.email}:`, error);
                }
            }
        }
    }
    
    // Function to initialize the system
    async function initializePrometheusSystem() {
        console.log('🚀 Initializing PROMETHEUS Trading System...');
        
        // Create admin account
        const adminCreated = await createAdminAccount();
        
        if (adminCreated) {
            // Create demo users
            await createDemoUsers();
            
            console.log('🎉 PROMETHEUS System Initialization Complete!');
            console.log('');
            console.log('🔑 ADMIN LOGIN CREDENTIALS:');
            console.log('📧 Email: admin@prometheus-neural-forge.com');
            console.log('🔑 Password: PrometheusAdmin2025!');
            console.log('🔗 Admin Portal: https://ai-mass-trading.web.app/admin.html');
            console.log('');
            console.log('👥 Demo Users Created:');
            console.log('📧 demo1@prometheus-trading.com | Password: Demo2025!');
            console.log('📧 demo2@prometheus-trading.com | Password: Demo2025!');
            console.log('📧 live1@prometheus-trading.com | Password: Live2025!');
            console.log('📧 live2@prometheus-trading.com | Password: Live2025!');
            console.log('');
            console.log('🎯 Next Steps:');
            console.log('1. Login to admin portal');
            console.log('2. Upgrade demo users to live trading');
            console.log('3. Enable real money trading');
            console.log('4. Start AI learning system');
        } else {
            console.error('❌ Failed to initialize system');
        }
    }
    
    // Auto-initialize when script loads
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializePrometheusSystem);
    } else {
        initializePrometheusSystem();
    }
}

// Export for manual execution
window.prometheusAdminSetup = {
    ADMIN_CREDENTIALS,
    createAdminAccount: () => createAdminAccount(),
    createDemoUsers: () => createDemoUsers(),
    initializeSystem: () => initializePrometheusSystem()
};
