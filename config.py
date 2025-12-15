"""
Configuration file for Index Data Analysis app.
Contains app setup, CSS styles, and constants.
"""

# Store IDs
STORE_RAW = "store_raw_df"
STORE_META = "store_meta"
STORE_A = "store_raw_a"
STORE_B = "store_raw_b"

# Month options for date pickers
MONTH_OPTIONS = [{"label": m, "value": i} for i, m in enumerate(
    ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"], start=1
)]

# Custom CSS and HTML template
APP_INDEX_STRING = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                margin: 0;
                padding: 0;
                border: none !important;
                transition: background-color 0.3s ease, color 0.3s ease;
            }
            html {
                margin: 0;
                padding: 0;
                border: none !important;
            }
            #react-entry-point {
                margin: 0;
                padding: 0;
                border: none !important;
            }
            ._dash-loading {
                margin: 0;
                padding: 0;
            }
            #app-container {
                transition: background-color 0.3s ease, color 0.3s ease;
            }
            #navbar-container {
                transition: background-color 0.3s ease, color 0.3s ease;
            }
            #page-content {
                transition: color 0.3s ease;
            }
            /* Upload box hover effect */
            [id="uploader"]:hover, [id="uploader-a"]:hover, [id="uploader-b"]:hover {
                border-color: rgba(0,200,150,0.6) !important;
                background: rgba(0,200,150,0.1) !important;
                transform: scale(1.01);
                box-shadow: 0 4px 16px rgba(0,200,150,0.2) !important;
            }
            [id="uploader"]:hover span:last-child, [id="uploader-a"]:hover span:last-child, [id="uploader-b"]:hover span:last-child {
                opacity: 1 !important;
                transform: scale(1.1);
            }
            /* Feature card hover effects */
            a[href="/single"] > div,
            a[href="/cross"] > div {
                position: relative;
            }
            a[href="/single"]:hover > div,
            a[href="/cross"]:hover > div {
                transform: translateY(-8px);
                box-shadow: 0 16px 40px rgba(0,0,0,0.3), 0 8px 16px rgba(0,0,0,0.2) !important;
            }
            a[href="/single"]:active > div,
            a[href="/cross"]:active > div {
                transform: translateY(-4px);
            }
            /* Feature card shine effect on hover */
            a[href="/single"] > div::before,
            a[href="/cross"] > div::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
                transition: left 0.5s;
            }
            a[href="/single"]:hover > div::before,
            a[href="/cross"]:hover > div::before {
                left: 100%;
            }
            /* DataTable dark theme styles */
            .dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner table {
                background-color: #1a1a1a !important;
                color: rgba(255,255,255,0.9) !important;
            }
            .dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner table thead th {
                background-color: #252525 !important;
                color: rgba(255,255,255,0.95) !important;
                border-color: rgba(0,200,150,0.3) !important;
            }
            .dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner table tbody tr {
                background-color: #1a1a1a !important;
            }
            .dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner table tbody tr:nth-child(even) {
                background-color: #222222 !important;
            }
            .dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner table tbody tr:hover {
                background-color: rgba(0,200,150,0.15) !important;
            }
            .dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner table tbody td {
                border-color: rgba(255,255,255,0.1) !important;
                color: rgba(255,255,255,0.9) !important;
            }
            /* Dark theme for form inputs */
            .Select-control, .Select-input, .Select-placeholder, .Select-value, .Select-value-label {
                background-color: rgba(255,255,255,0.1) !important;
                color: rgba(255,255,255,0.9) !important;
                border-color: rgba(255,255,255,0.2) !important;
            }
            .Select-menu-outer {
                background-color: #1a1a1a !important;
                border-color: rgba(255,255,255,0.2) !important;
            }
            .Select-option {
                background-color: #1a1a1a !important;
                color: rgba(255,255,255,0.9) !important;
            }
            .Select-option.is-focused {
                background-color: rgba(0,200,150,0.2) !important;
            }
            .Select-option.is-selected {
                background-color: rgba(0,200,150,0.4) !important;
            }
            input[type="text"], input[type="number"], input[type="date"] {
                background-color: rgba(255,255,255,0.1) !important;
                color: rgba(255,255,255,0.9) !important;
                border: 1px solid rgba(255,255,255,0.2) !important;
                border-radius: 4px !important;
                padding: 6px 8px !important;
            }
            input[type="text"]:focus, input[type="number"]:focus, input[type="date"]:focus {
                border-color: rgba(0,200,150,0.6) !important;
                outline: none !important;
                box-shadow: 0 0 0 2px rgba(0,200,150,0.2) !important;
            }
            input[type="text"]::placeholder, input[type="number"]::placeholder {
                color: rgba(255,255,255,0.5) !important;
            }
            .DateInput {
                background-color: rgba(255,255,255,0.1) !important;
            }
            .DateInput_input {
                background-color: rgba(255,255,255,0.1) !important;
                color: rgba(255,255,255,0.9) !important;
                border-color: rgba(255,255,255,0.2) !important;
                font-size: 14px !important;
                padding: 8px 10px !important;
            }
            .DateInput_input__focused {
                border-color: rgba(0,200,150,0.6) !important;
                box-shadow: 0 0 0 2px rgba(0,200,150,0.2) !important;
            }
            .DateRangePickerInput {
                background-color: rgba(255,255,255,0.1) !important;
                border-color: rgba(255,255,255,0.2) !important;
                border-radius: 4px !important;
            }
            .DateRangePickerInput__withBorder {
                border-radius: 4px !important;
            }
            .DateRangePickerInput__disabled {
                background-color: rgba(255,255,255,0.05) !important;
            }
            .DateRangePickerInput_arrow {
                border-left-color: rgba(255,255,255,0.5) !important;
            }
            .DateRangePickerInput_arrow_svg {
                fill: rgba(255,255,255,0.7) !important;
            }
            /* Fix DatePickerRange clear button overlap */
            .DateInput__close {
                position: absolute !important;
                right: 8px !important;
                top: 50% !important;
                transform: translateY(-50%) !important;
                z-index: 10 !important;
                background: rgba(255,255,255,0.1) !important;
                border-radius: 50% !important;
                width: 20px !important;
                height: 20px !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                cursor: pointer !important;
            }
            .DateInput__close:hover {
                background: rgba(255,255,255,0.2) !important;
            }
            .DateInput__close svg {
                width: 12px !important;
                height: 12px !important;
            }
            .DateInput {
                position: relative !important;
                padding-right: 32px !important;
            }
            .DateRangePickerInput__withBorder {
                position: relative !important;
            }
            .DayPicker {
                background-color: #1a1a1a !important;
                color: rgba(255,255,255,0.9) !important;
                border: 1px solid rgba(255,255,255,0.2) !important;
                border-radius: 8px !important;
            }
            .DayPicker__week-header {
                color: rgba(255,255,255,0.7) !important;
            }
            .DayPicker-Day {
                color: rgba(255,255,255,0.9) !important;
            }
            .DayPicker-Day--selected {
                background-color: rgba(0,200,150,0.6) !important;
                color: white !important;
            }
            .DayPicker-Day--hovered {
                background-color: rgba(0,200,150,0.3) !important;
            }
            .DayPicker-Day--outside {
                color: rgba(255,255,255,0.3) !important;
            }
            /* Color-coded radio buttons for Drop (red) and Gain (green) */
            #window-size-drop input[type="radio"],
            #min-threshold-drop input[type="radio"],
            #snap-month-drop input[type="checkbox"] {
                accent-color: rgba(239,68,68,0.8) !important;
            }
            #window-size-gain input[type="radio"],
            #min-threshold-gain input[type="radio"],
            #snap-month-gain input[type="checkbox"] {
                accent-color: rgba(34,197,94,0.8) !important;
            }
            /* Default accent for other radio/checkboxes */
            input[type="radio"] {
                accent-color: rgba(0,200,150,0.8) !important;
            }
            input[type="checkbox"] {
                accent-color: rgba(0,200,150,0.8) !important;
            }
            /* Improved spacing for radio buttons and inputs */
            .RadioItems, .Checklist {
                margin-bottom: 8px !important;
            }
            .RadioItems label, .Checklist label {
                margin-right: 12px !important;
                margin-bottom: 4px !important;
            }
            /* Better visual grouping for custom inputs */
            input[type="number"] {
                margin-top: 4px !important;
            }
            /* Responsive grid support */
            @media (max-width: 768px) {
                [style*="gridTemplateColumns"] {
                    grid-template-columns: 1fr !important;
                }
            }
            /* Responsive feature cards */
            @media (max-width: 900px) {
                a[href="/single"] > div,
                a[href="/cross"] > div {
                    max-width: 100% !important;
                    min-height: 340px !important;
                }
            }
            @media (max-width: 480px) {
                a[href="/single"] > div,
                a[href="/cross"] > div {
                    padding: 28px 20px !important;
                    min-height: 320px !important;
                }
            }
            /* Focus states for accessibility */
            button:focus-visible, input:focus-visible, select:focus-visible {
                outline: none !important;
            }
            /* Feature card focus states */
            a[href="/single"]:focus-visible > div,
            a[href="/cross"]:focus-visible > div {
                outline: 3px solid rgba(102,126,234,0.6) !important;
                outline-offset: 4px;
            }
            a[href="/cross"]:focus-visible > div {
                outline-color: rgba(240,147,251,0.6) !important;
            }
            /* Hover states for buttons */
            button:hover:not(:disabled) {
                transform: translateY(-1px);
                box-shadow: 0 6px 16px rgba(0,0,0,0.2) !important;
            }
            button:active:not(:disabled) {
                transform: translateY(0);
            }
            /* Disabled state styling */
            button:disabled, input:disabled, select:disabled {
                opacity: 0.5 !important;
                cursor: not-allowed !important;
            }
            /* Improved input heights for consistency */
            input[type="text"], input[type="number"] {
                height: 40px !important;
                min-height: 40px !important;
            }
            /* Card hover effect */
            [style*="background"][style*="#121821"]:hover {
                box-shadow: 0 6px 16px rgba(0,0,0,0.4) !important;
            }
            /* Responsive button styling */
            @media (max-width: 768px) {
                #analyze, #x-analyze {
                    width: 100% !important;
                    float: none !important;
                }
                .card-footer {
                    text-align: center !important;
                }
            }
            /* DataTable pagination styling */
            .dash-table-toolbar {
                background-color: #1a1a1a !important;
                color: rgba(255,255,255,0.9) !important;
                padding: 8px !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                gap: 8px !important;
                flex-wrap: wrap !important;
            }
            /* Style navigation buttons */
            .dash-table-toolbar .previous-page, 
            .dash-table-toolbar .next-page,
            .dash-table-toolbar .first-page,
            .dash-table-toolbar .last-page {
                background-color: rgba(255,255,255,0.1) !important;
                color: rgba(255,255,255,0.9) !important;
                border: 1px solid rgba(255,255,255,0.2) !important;
                border-radius: 4px !important;
                padding: 6px 12px !important;
                margin: 0 !important;
                min-width: 36px !important;
                height: 32px !important;
                cursor: pointer !important;
                display: inline-flex !important;
                align-items: center !important;
                justify-content: center !important;
                font-size: 14px !important;
                line-height: 1 !important;
                box-sizing: border-box !important;
            }
            .dash-table-toolbar .previous-page:hover, 
            .dash-table-toolbar .next-page:hover,
            .dash-table-toolbar .first-page:hover,
            .dash-table-toolbar .last-page:hover {
                background-color: rgba(0,200,150,0.2) !important;
                border-color: rgba(0,200,150,0.4) !important;
            }
            .dash-table-toolbar .previous-page:disabled, 
            .dash-table-toolbar .next-page:disabled,
            .dash-table-toolbar .first-page:disabled,
            .dash-table-toolbar .last-page:disabled {
                opacity: 0.3 !important;
                cursor: not-allowed !important;
            }
            /* Fix duplicate page number - hide all spans/divs that might show duplicate page number */
            /* Target the container that holds the page input */
            .dash-table-toolbar > div {
                display: inline-flex !important;
                align-items: center !important;
                position: relative !important;
                height: 32px !important;
            }
            /* Hide ALL child elements in the input container EXCEPT the input itself */
            .dash-table-toolbar > div:has(input[type="number"]) > span,
            .dash-table-toolbar > div:has(input[type="number"]) > div:not(:has(input)),
            .dash-table-toolbar > div:has(input[type="number"]) > label,
            .dash-table-toolbar > div:has(input[type="number"]) > *:not(input[type="number"]) {
                display: none !important;
                visibility: hidden !important;
            }
            /* Style the page number input */
            .dash-table-toolbar input[type="number"] {
                background-color: rgba(255,255,255,0.1) !important;
                color: rgba(255,255,255,0.9) !important;
                border: 1px solid rgba(255,255,255,0.2) !important;
                border-radius: 4px !important;
                padding: 6px 10px !important;
                width: 60px !important;
                min-width: 60px !important;
                max-width: 60px !important;
                text-align: center !important;
                font-weight: 500 !important;
                font-size: 14px !important;
                line-height: 1.2 !important;
                height: 32px !important;
                -moz-appearance: textfield !important;
                box-sizing: border-box !important;
                display: inline-block !important;
                visibility: visible !important;
                position: relative !important;
                z-index: 1 !important;
            }
            /* Hide spinner buttons on number input */
            .dash-table-toolbar input[type="number"]::-webkit-inner-spin-button,
            .dash-table-toolbar input[type="number"]::-webkit-outer-spin-button {
                -webkit-appearance: none !important;
                margin: 0 !important;
            }
            /* Hide any duplicate inputs */
            .dash-table-toolbar input[type="number"]:not(:first-of-type) {
                display: none !important;
            }
            /* Hide any pseudo-elements that might duplicate content */
            .dash-table-toolbar > div::before,
            .dash-table-toolbar > div::after,
            .dash-table-toolbar input[type="number"]::before,
            .dash-table-toolbar input[type="number"]::after {
                display: none !important;
                content: none !important;
            }
            /* Keep the "/ total" text visible - it's in the last div */
            .dash-table-toolbar > div:last-child:not(:has(input)) {
                display: inline-block !important;
                color: rgba(255,255,255,0.7) !important;
                font-size: 14px !important;
                margin-left: 4px !important;
                visibility: visible !important;
            }
            .dash-table-toolbar > div:last-child:not(:has(input)) > * {
                display: inline !important;
                visibility: visible !important;
            }
            /* Additional fix: Hide any elements with class names that suggest duplicate page numbers */
            .dash-table-toolbar .page-number,
            .dash-table-toolbar [class*="current-page"],
            .dash-table-toolbar [class*="page-input"] > span:not(:last-child),
            .dash-table-toolbar [class*="page-input"] > div:not(:has(input)) {
                display: none !important;
                visibility: hidden !important;
            }
            /* Prevent any pseudo-elements from duplicating content */
            .dash-table-toolbar input[type="number"]::before,
            .dash-table-toolbar input[type="number"]::after {
                display: none !important;
                content: none !important;
            }
            
            /* Make drawdown loading spinner bigger and more prominent */
            #drawdown-loading ._dash-loading-callback {
                width: 100px !important;
                height: 100px !important;
            }
            #drawdown-loading ._dash-loading {
                margin: 0 !important;
            }
            #drawdown-loading .dash-spinner {
                width: 100px !important;
                height: 100px !important;
            }
            #drawdown-loading .dash-spinner > div {
                width: 100px !important;
                height: 100px !important;
                border-width: 8px !important;
            }
            /* Center the spinner properly */
            ._dash-loading-callback {
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
            }
        </style>
        <script>
            // Fix duplicate page number in DataTable pagination
            function fixPaginationDuplicates() {
                const toolbars = document.querySelectorAll('.dash-table-toolbar');
                toolbars.forEach(toolbar => {
                    // Find the input container
                    const inputContainers = Array.from(toolbar.children).filter(div => {
                        return div.querySelector('input[type="number"]');
                    });
                    
                    inputContainers.forEach(container => {
                        const input = container.querySelector('input[type="number"]');
                        if (!input) return;
                        
                        // Hide all children except the input itself
                        Array.from(container.children).forEach(child => {
                            if (child !== input && child.tagName !== 'SCRIPT') {
                                child.style.display = 'none';
                                child.style.visibility = 'hidden';
                            }
                        });
                        
                        // Remove any text nodes or overlays
                        const walker = document.createTreeWalker(
                            container,
                            NodeFilter.SHOW_TEXT,
                            null,
                            false
                        );
                        let node;
                        while (node = walker.nextNode()) {
                            if (node.parentElement !== input && node.textContent.trim() === input.value) {
                                node.textContent = '';
                            }
                        }
                    });
                });
            }
            
            // Run on page load and after any updates
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', fixPaginationDuplicates);
            } else {
                fixPaginationDuplicates();
            }
            
            // Use MutationObserver to fix duplicates when table updates
            const observer = new MutationObserver(function(mutations) {
                let shouldFix = false;
                mutations.forEach(function(mutation) {
                    if (mutation.addedNodes.length > 0) {
                        mutation.addedNodes.forEach(function(node) {
                            if (node.nodeType === 1 && (
                                node.classList.contains('dash-table-toolbar') ||
                                node.querySelector('.dash-table-toolbar')
                            )) {
                                shouldFix = true;
                            }
                        });
                    }
                });
                if (shouldFix) {
                    setTimeout(fixPaginationDuplicates, 100);
                }
            });
            
            observer.observe(document.body, {
                childList: true,
                subtree: true
            });
        </script>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

