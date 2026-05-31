/*
==========================================================================
Chi Tiêu Cá Nhân - JavaScript chức năng
Mô tả: Xử lý các tương tác giao diện cho ứng dụng quản lý chi tiêu
Phiên bản: 1.0
==========================================================================
*/

(function () {
    'use strict';

    /* ========================================
       Theme Toggle
    ======================================== */
    function initThemeToggle() {
        const themeSwitch = document.getElementById('themeSwitch');
        const themeToggleBtn = document.getElementById('themeToggle');
        const html = document.documentElement;

        // Load saved theme
        const savedTheme = localStorage.getItem('theme') || 'dark';
        html.setAttribute('data-theme', savedTheme);

        // Dashboard theme switch (sidebar)
        if (themeSwitch) {
            themeSwitch.addEventListener('click', function () {
                const currentTheme = html.getAttribute('data-theme');
                const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
                html.setAttribute('data-theme', newTheme);
                localStorage.setItem('theme', newTheme);

                // Update dark mode toggle in settings if exists
                updateDarkModeToggle();
            });
        }

        // Login page theme toggle button
        if (themeToggleBtn) {
            themeToggleBtn.addEventListener('click', function () {
                const currentTheme = html.getAttribute('data-theme');
                const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
                html.setAttribute('data-theme', newTheme);
                localStorage.setItem('theme', newTheme);
            });
        }
    }

    /* ========================================
       Dark Mode Toggle (Settings Page)
    ======================================== */
    function updateDarkModeToggle() {
        const darkModeToggle = document.getElementById('darkModeToggle');
        const html = document.documentElement;

        if (darkModeToggle) {
            if (html.getAttribute('data-theme') === 'dark') {
                darkModeToggle.classList.add('active');
            } else {
                darkModeToggle.classList.remove('active');
            }
        }
    }

    function initDarkModeToggle() {
        const darkModeToggle = document.getElementById('darkModeToggle');
        const themeSwitch = document.getElementById('themeSwitch');

        updateDarkModeToggle();

        if (darkModeToggle && themeSwitch) {
            darkModeToggle.addEventListener('click', function () {
                themeSwitch.click();
            });
        }
    }

    /* ========================================
       Mobile Menu
    ======================================== */
    function initMobileMenu() {
        const mobileMenuToggle = document.getElementById('mobileMenuToggle');
        const sidebar = document.getElementById('sidebar');
        const sidebarOverlay = document.getElementById('sidebarOverlay');

        function toggleMobileMenu() {
            if (mobileMenuToggle && sidebar && sidebarOverlay) {
                mobileMenuToggle.classList.toggle('active');
                sidebar.classList.toggle('active');
                sidebarOverlay.classList.toggle('active');
                document.body.style.overflow = sidebar.classList.contains('active') ? 'hidden' : '';
            }
        }

        if (mobileMenuToggle) {
            mobileMenuToggle.addEventListener('click', toggleMobileMenu);
        }

        if (sidebarOverlay) {
            sidebarOverlay.addEventListener('click', toggleMobileMenu);
        }

        // Close menu when clicking nav items
        document.querySelectorAll('.nav-item').forEach(function (item) {
            item.addEventListener('click', function () {
                if (window.innerWidth <= 1024 && sidebar && sidebar.classList.contains('active')) {
                    toggleMobileMenu();
                }
            });
        });

        // Close menu on window resize
        window.addEventListener('resize', function () {
            if (window.innerWidth > 1024 && sidebar && sidebar.classList.contains('active')) {
                toggleMobileMenu();
            }
        });
    }

    /* ========================================
       Toggle Switches
    ======================================== */
    function initToggleSwitches() {
        document.querySelectorAll('.toggle-switch').forEach(function (toggle) {
            // Skip dark mode toggle as it's handled separately
            if (toggle.id !== 'darkModeToggle') {
                toggle.addEventListener('click', function () {
                    toggle.classList.toggle('active');
                });
            }
        });
    }

    /* ========================================
       Sao chép số tài khoản
    ======================================== */
    function initCopyButtons() {
        document.querySelectorAll('.copy-btn').forEach(function (btn) {
            btn.addEventListener('click', function () {
                // Tìm phần tử chứa thông tin mô tả ví
                const moTaElement = btn.parentElement.querySelector('.vi-mo-ta');
                if (moTaElement) {
                    const text = moTaElement.textContent;
                    navigator.clipboard.writeText(text).then(function () {
                        // Hiển thị trạng thái thành công
                        btn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#6b8e6b" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>';

                        // Đặt lại sau 2 giây
                        setTimeout(function () {
                            btn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/></svg>';
                        }, 2000);
                    });
                }
            });
        });
    }

    /* ========================================
       Settings Tabs
    ======================================== */
    function initSettingsTabs() {
        document.querySelectorAll('.settings-tab').forEach(function (tab) {
            tab.addEventListener('click', function () {
                // Remove active from all tabs
                document.querySelectorAll('.settings-tab').forEach(function (t) {
                    t.classList.remove('active');
                });

                // Remove active from all content
                document.querySelectorAll('.settings-content').forEach(function (c) {
                    c.classList.remove('active');
                });

                // Add active to clicked tab
                tab.classList.add('active');

                // Show corresponding content
                const targetId = tab.dataset.tab;
                const targetContent = document.getElementById(targetId);
                if (targetContent) {
                    targetContent.classList.add('active');
                }
            });
        });
    }





    /* ========================================
       Tìm kiếm giao dịch
    ======================================== */
    function initSearch() {
        const searchInput = document.getElementById('searchInput');

        if (searchInput) {
            searchInput.addEventListener('input', function (e) {
                const search = e.target.value.toLowerCase();

                // Tìm kiếm trong bảng giao dịch theo tên danh mục
                document.querySelectorAll('.giao-dich-table tbody tr').forEach(function (row) {
                    const tenElement = row.querySelector('.transaction-category');

                    if (tenElement) {
                        const ten = tenElement.textContent.toLowerCase();
                        row.style.display = ten.includes(search) ? '' : 'none';
                    } else {
                        // Nếu không có class cụ thể, tìm trong toàn bộ hàng
                        const text = row.textContent.toLowerCase();
                        row.style.display = text.includes(search) ? '' : 'none';
                    }
                });
            });
        }
    }

    /* ========================================
       Checkbox Toggle
    ======================================== */
    function initCheckboxes() {
        document.querySelectorAll('.checkbox-wrapper').forEach(function (wrapper) {
            wrapper.addEventListener('click', function () {
                const checkbox = wrapper.querySelector('.checkbox');
                if (checkbox) {
                    checkbox.classList.toggle('checked');
                }
            });
        });
    }

    /* ========================================
       Password Toggle
    ======================================== */
    function initPasswordToggle() {
        document.querySelectorAll('.password-toggle').forEach(function (btn) {
            btn.addEventListener('click', function () {
                const targetId = btn.dataset.target;
                const input = document.getElementById(targetId);

                if (input) {
                    const type = input.type === 'password' ? 'text' : 'password';
                    input.type = type;
                }
            });
        });
    }

    /* ========================================
       Password Strength Meter
    ======================================== */
    function initPasswordStrength() {
        const passwordInput = document.getElementById('registerPassword');
        const strengthBars = document.querySelectorAll('.strength-bar');

        if (passwordInput && strengthBars.length > 0) {
            passwordInput.addEventListener('input', function () {
                const password = passwordInput.value;
                let strength = 0;

                if (password.length >= 8) strength++;
                if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++;
                if (/\d/.test(password)) strength++;
                if (/[^a-zA-Z0-9]/.test(password)) strength++;

                strengthBars.forEach(function (bar, index) {
                    bar.classList.remove('weak', 'medium', 'strong');
                    if (index < strength) {
                        if (strength <= 1) bar.classList.add('weak');
                        else if (strength <= 2) bar.classList.add('medium');
                        else bar.classList.add('strong');
                    }
                });
            });
        }
    }

    /* ========================================
       Tab Đăng nhập / Đăng ký
    ======================================== */
    function initAuthTabs() {
        const authTabs = document.querySelectorAll('.auth-tab');
        const loginForm = document.getElementById('loginForm');
        const registerForm = document.getElementById('registerForm');
        const formHeader = document.querySelector('.form-header');

        authTabs.forEach(function (tab) {
            tab.addEventListener('click', function () {
                authTabs.forEach(function (t) {
                    t.classList.remove('active');
                });
                tab.classList.add('active');

                if (tab.dataset.form === 'login') {
                    if (loginForm) loginForm.classList.add('active');
                    if (registerForm) registerForm.classList.remove('active');
                    if (formHeader) {
                        formHeader.querySelector('h1').textContent = 'Chào mừng trở lại';
                        formHeader.querySelector('p').textContent = 'Nhập thông tin để truy cập tài khoản';
                    }
                } else {
                    if (registerForm) registerForm.classList.add('active');
                    if (loginForm) loginForm.classList.remove('active');
                    if (formHeader) {
                        formHeader.querySelector('h1').textContent = 'Tạo tài khoản mới';
                        formHeader.querySelector('p').textContent = 'Bắt đầu quản lý chi tiêu của bạn ngay hôm nay';
                    }
                }
            });
        });

        // Chuyển đổi nhanh giữa các form
        const switchToRegister = document.getElementById('switchToRegister');
        const switchToLogin = document.getElementById('switchToLogin');

        if (switchToRegister && authTabs[1]) {
            switchToRegister.addEventListener('click', function (e) {
                e.preventDefault();
                authTabs[1].click();
            });
        }

        if (switchToLogin && authTabs[0]) {
            switchToLogin.addEventListener('click', function (e) {
                e.preventDefault();
                authTabs[0].click();
            });
        }
    }



    /* ========================================
       Nhóm Dropdown Menu
    ======================================== */
    function initNhomDropdown() {
        const nhomButton = document.querySelector('.dropdown-toggle');
        const nhomMenu = document.getElementById('nhomMenu');

        if (nhomButton && nhomMenu) {
            // Toggle menu when clicking button
            nhomButton.addEventListener('click', function (event) {
                event.preventDefault();
                event.stopPropagation();
                const isActive = nhomMenu.classList.contains('active');
                if (isActive) {
                    nhomMenu.classList.remove('active');
                    nhomButton.classList.remove('active');
                } else {
                    nhomMenu.classList.add('active');
                    nhomButton.classList.add('active');
                }
            });

            // Close menu when clicking on a submenu item
            const dropdownItems = nhomMenu.querySelectorAll('.dropdown-item');
            dropdownItems.forEach(function (item) {
                item.addEventListener('click', function (event) {
                    event.stopPropagation();
                    // Don't prevent default - let it navigate
                    // Just close the menu
                    setTimeout(function () {
                        nhomMenu.classList.remove('active');
                        nhomButton.classList.remove('active');
                    }, 50);
                });
            });

            // Close menu when clicking outside
            document.addEventListener('click', function (event) {
                if (nhomMenu.classList.contains('active')) {
                    if (!nhomButton.contains(event.target) && !nhomMenu.contains(event.target)) {
                        nhomMenu.classList.remove('active');
                        nhomButton.classList.remove('active');
                    }
                }
            });
        }
    }

    /* ========================================
       Initialize All
    ======================================== */
    function init() {
        initThemeToggle();
        initDarkModeToggle();
        initMobileMenu();
        initToggleSwitches();
        initCopyButtons();
        initSettingsTabs();
        initSearch();
        initCheckboxes();
        initPasswordToggle();
        initPasswordStrength();
        initAuthTabs();
        initNhomDropdown();
    }

    // Run on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();


