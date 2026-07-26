/* ============================================
   Green Hospital Ltd - Production JavaScript
   ============================================ */

(function() {
    'use strict';

    // ===== Mobile Menu Toggle =====
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const navLinks = document.getElementById('navLinks');
    
    if (mobileMenuBtn && navLinks) {
        mobileMenuBtn.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            const isActive = navLinks.classList.contains('active');
            mobileMenuBtn.setAttribute('aria-expanded', isActive);
            mobileMenuBtn.querySelector('i').className = isActive 
                ? 'fa-solid fa-times' 
                : 'fa-solid fa-bars';
            document.body.style.overflow = isActive ? 'hidden' : '';
        });

        // Close menu when clicking a link
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth <= 768) {
                    navLinks.classList.remove('active');
                    mobileMenuBtn.setAttribute('aria-expanded', 'false');
                    mobileMenuBtn.querySelector('i').className = 'fa-solid fa-bars';
                    document.body.style.overflow = '';
                }
            });
        });

        // Close on outside click
        document.addEventListener('click', (e) => {
            if (!navLinks.contains(e.target) && !mobileMenuBtn.contains(e.target) && navLinks.classList.contains('active')) {
                navLinks.classList.remove('active');
                mobileMenuBtn.setAttribute('aria-expanded', 'false');
                mobileMenuBtn.querySelector('i').className = 'fa-solid fa-bars';
                document.body.style.overflow = '';
            }
        });
    }
    // ===== Hero Slider =====
    const heroSlider = document.getElementById('heroSlider');
    const heroSlides = document.querySelectorAll('.hero-slide');
    const heroPrevBtn = document.getElementById('heroPrevBtn');
    const heroNextBtn = document.getElementById('heroNextBtn');
    const heroDots = document.querySelectorAll('#heroSliderDots .dot');

    if (heroSlider && heroSlides.length > 0) {
        let currentSlide = 0;
        const totalSlides = heroSlides.length;
        let slideInterval;

        function goToSlide(index) {
            if (index < 0) index = totalSlides - 1;
            if (index >= totalSlides) index = 0;
            currentSlide = index;
            
            heroSlider.style.transform = `translateX(-${currentSlide * 100}%)`;
            
            heroDots.forEach((dot, i) => {
                dot.classList.toggle('active', i === currentSlide);
            });
        }

        function nextSlide() {
            goToSlide(currentSlide + 1);
        }

        function prevSlide() {
            goToSlide(currentSlide - 1);
        }

        function startAutoSlide() {
            stopAutoSlide();
            slideInterval = setInterval(nextSlide, 5000);
        }

        function stopAutoSlide() {
            if (slideInterval) clearInterval(slideInterval);
        }

        if (heroNextBtn) {
            heroNextBtn.addEventListener('click', () => {
                nextSlide();
                startAutoSlide();
            });
        }

        if (heroPrevBtn) {
            heroPrevBtn.addEventListener('click', () => {
                prevSlide();
                startAutoSlide();
            });
        }

        heroDots.forEach(dot => {
            dot.addEventListener('click', (e) => {
                const slideIdx = parseInt(e.target.dataset.slide);
                goToSlide(slideIdx);
                startAutoSlide();
            });
        });

        // Touch swipe support for mobile
        let touchStartX = 0;
        let touchEndX = 0;
        let touchStartY = 0;
        let touchEndY = 0;

        heroSlider.addEventListener('touchstart', (e) => {
            touchStartX = e.changedTouches[0].screenX;
            touchStartY = e.changedTouches[0].screenY;
            stopAutoSlide();
        }, { passive: true });

        heroSlider.addEventListener('touchend', (e) => {
            touchEndX = e.changedTouches[0].screenX;
            touchEndY = e.changedTouches[0].screenY;
            
            const diffX = touchStartX - touchEndX;
            const diffY = touchStartY - touchEndY;
            
            if (Math.abs(diffX) > 50 && Math.abs(diffX) > Math.abs(diffY)) {
                if (diffX > 0) {
                    nextSlide();
                } else {
                    prevSlide();
                }
            }
            startAutoSlide();
        }, { passive: true });

        // Pause on hover
        heroSlider.addEventListener('mouseenter', stopAutoSlide);
        heroSlider.addEventListener('mouseleave', startAutoSlide);

        // Start initial timer
        startAutoSlide();
    }

    // ===== Scroll to Top Button =====
    const scrollTopBtn = document.getElementById('scrollToTop');
    if (scrollTopBtn) {
        window.addEventListener('scroll', () => {
            if (window.pageYOffset > 300) {
                scrollTopBtn.classList.add('visible');
            } else {
                scrollTopBtn.classList.remove('visible');
            }
        });
        
        scrollTopBtn.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // ===== Header scroll effect =====
    const header = document.querySelector('.header');
    if (header) {
        let lastScroll = 0;
        window.addEventListener('scroll', () => {
            const currentScroll = window.pageYOffset;
            if (currentScroll > 100) {
                header.style.boxShadow = '0 2px 20px rgba(0,0,0,0.08)';
            } else {
                header.style.boxShadow = '0 1px 2px rgba(0,0,0,0.05)';
            }
            lastScroll = currentScroll;
        });
    }

    // ===== FAQ Accordion =====
    const faqQuestions = document.querySelectorAll('.faq-question');
    faqQuestions.forEach(q => {
        q.addEventListener('click', () => {
            const item = q.parentElement;
            const isActive = item.classList.contains('active');
            
            // Close all
            document.querySelectorAll('.faq-item').forEach(faq => {
                faq.classList.remove('active');
            });
            
            // Open clicked (if not already open)
            if (!isActive) {
                item.classList.add('active');
            }
        });
    });

    // ===== Department Filter (doctors.html) =====
    const filterBtns = document.querySelectorAll('.filter-btn');
    const doctorCards = document.querySelectorAll('.doctor-card[data-department]');
    
    if (filterBtns.length > 0 && doctorCards.length > 0) {
        filterBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const filter = btn.dataset.filter;
                
                // Update active button
                filterBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                
                // Filter cards with animation
                doctorCards.forEach(card => {
                    const dept = card.dataset.department;
                    if (filter === 'all' || dept === filter) {
                        card.style.display = '';
                        setTimeout(() => {
                            card.style.opacity = '1';
                            card.style.transform = 'translateY(0)';
                        }, 10);
                    } else {
                        card.style.opacity = '0';
                        card.style.transform = 'translateY(20px)';
                        setTimeout(() => {
                            card.style.display = 'none';
                        }, 300);
                    }
                });
            });
        });
    }

    // ===== Doctor Search =====
    const doctorSearch = document.getElementById('doctorSearch');
    if (doctorSearch) {
        let debounceTimer;
        doctorSearch.addEventListener('input', (e) => {
            clearTimeout(debounceTimer);
            const query = e.target.value.trim().toLowerCase();
            debounceTimer = setTimeout(() => {
                doctorCards.forEach(card => {
                    const name = (card.dataset.name || card.textContent).toLowerCase();
                    const specialty = (card.dataset.specialty || '').toLowerCase();
                    const matches = !query || name.includes(query) || specialty.includes(query);
                    
                    if (matches) {
                        card.style.display = '';
                        setTimeout(() => {
                            card.style.opacity = '1';
                        }, 10);
                    } else {
                        card.style.opacity = '0';
                        setTimeout(() => {
                            card.style.display = 'none';
                        }, 300);
                    }
                });
            }, 200);
        });
    }

    // ===== Contact Form =====
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(contactForm);
            const submitBtn = contactForm.querySelector('button[type="submit"]');
            const originalBtnText = submitBtn.innerHTML;
            
            // Disable button
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> পাঠানো হচ্ছে...';
            
            // Remove previous messages
            const existingMsg = contactForm.querySelector('.form-message');
            if (existingMsg) existingMsg.remove();
            
            try {
                const response = await fetch('api/contact.php', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();
                
                const msgDiv = document.createElement('div');
                msgDiv.className = 'form-message ' + (data.success ? 'success' : 'error');
                msgDiv.innerHTML = data.success 
                    ? '<i class="fa-solid fa-circle-check"></i> ' + (data.message || 'আপনার বার্তা সফলভাবে পাঠানো হয়েছে। আমরা শিঘ্রই যোগাযোগ করবো।')
                    : '<i class="fa-solid fa-circle-xmark"></i> ' + (data.message || 'একটি সমস্যা হয়েছে। আবার চেষ্টা করুন।');
                
                contactForm.insertBefore(msgDiv, contactForm.firstChild);
                
                if (data.success) {
                    contactForm.reset();
                    setTimeout(() => msgDiv.remove(), 5000);
                }
                
                // Scroll to message
                msgDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
                
            } catch (err) {
                console.error('Form error:', err);
                const msgDiv = document.createElement('div');
                msgDiv.className = 'form-message error';
                msgDiv.innerHTML = '<i class="fa-solid fa-circle-xmark"></i> নেটওয়ার্ক সমস্যা। আবার চেষ্টা করুন অথবা সরাসরি কল করুন: <a href="tel:01988118833">01988-118833</a>';
                contactForm.insertBefore(msgDiv, contactForm.firstChild);
            } finally {
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalBtnText;
            }
        });
    }

    // ===== Appointment Form =====
    const appointmentForm = document.getElementById('appointmentForm');
    if (appointmentForm) {
        appointmentForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(appointmentForm);
            const submitBtn = appointmentForm.querySelector('button[type="submit"]');
            const originalBtnText = submitBtn.innerHTML;
            
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> বুকিং হচ্ছে...';
            
            const existingMsg = appointmentForm.querySelector('.form-message');
            if (existingMsg) existingMsg.remove();
            
            try {
                const response = await fetch('api/appointment.php', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();
                
                const msgDiv = document.createElement('div');
                msgDiv.className = 'form-message ' + (data.success ? 'success' : 'error');
                msgDiv.innerHTML = data.success 
                    ? '<i class="fa-solid fa-circle-check"></i> ' + (data.message || 'অ্যাপয়েন্টমেন্ট সফলভাবে বুক হয়েছে।')
                    : '<i class="fa-solid fa-circle-xmark"></i> ' + (data.message || 'একটি সমস্যা হয়েছে। আবার চেষ্টা করুন।');
                
                appointmentForm.insertBefore(msgDiv, appointmentForm.firstChild);
                
                if (data.success) {
                    appointmentForm.reset();
                    setTimeout(() => msgDiv.remove(), 8000);
                }
                
                msgDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
                
            } catch (err) {
                console.error('Form error:', err);
                const msgDiv = document.createElement('div');
                msgDiv.className = 'form-message error';
                msgDiv.innerHTML = '<i class="fa-solid fa-circle-xmark"></i> নেটওয়ার্ক সমস্যা। সরাসরি কল করুন: <a href="tel:01988118833">01988-118833</a>';
                appointmentForm.insertBefore(msgDiv, appointmentForm.firstChild);
            } finally {
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalBtnText;
            }
        });
    }

    // ===== Smooth scroll for anchor links =====
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const target = this.getAttribute('href');
            if (target === '#' || target === '#!') return;
            const targetEl = document.querySelector(target);
            if (targetEl) {
                e.preventDefault();
                targetEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    // ===== Animated counters =====
    const counters = document.querySelectorAll('.counter');
    if (counters.length > 0 && 'IntersectionObserver' in window) {
        const counterObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const counter = entry.target;
                    const target = parseInt(counter.dataset.target);
                    const duration = 1500;
                    const step = target / (duration / 16);
                    let current = 0;
                    
                    const update = () => {
                        current += step;
                        if (current < target) {
                            counter.textContent = Math.floor(current);
                            requestAnimationFrame(update);
                        } else {
                            counter.textContent = target;
                        }
                    };
                    update();
                    counterObserver.unobserve(counter);
                }
            });
        }, { threshold: 0.5 });
        
        counters.forEach(c => counterObserver.observe(c));
    }

    // ===== Lazy load images fallback =====
    if ('loading' in HTMLImageElement.prototype) {
        // Native lazy loading supported
    } else {
        // Fallback: IntersectionObserver
        const lazyImages = document.querySelectorAll('img[loading="lazy"]');
        if (lazyImages.length > 0 && 'IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src || img.src;
                        img.classList.add('loaded');
                        imageObserver.unobserve(img);
                    }
                });
            });
            lazyImages.forEach(img => imageObserver.observe(img));
        }
    }

    // ===== Auto-set year in footer =====
    const yearEl = document.getElementById('currentYear');
    if (yearEl) {
        yearEl.textContent = new Date().getFullYear();
    }

    // ===== Service Worker Registration =====
    if ('serviceWorker' in navigator && location.protocol === 'https:') {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('/service-worker.js')
                .then(reg => console.log('SW registered:', reg.scope))
                .catch(err => console.log('SW registration failed:', err));
        });
    }

})();
