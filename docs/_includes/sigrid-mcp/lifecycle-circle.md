{%- comment -%}
The agentic lifecycle diagram, described on the developer guides page. Pass the stages this page is
about with active="plan,improve"; the stages you leave out are greyed out. Omit it to show all four.
{%- endcomment -%}
{%- assign stages = "grounding,plan,prevent,improve" | split: "," -%}
{%- assign active = include.active | default: "grounding,plan,prevent,improve" | split: "," -%}
{%- capture disabled -%}
{%- for stage in stages -%}{%- unless active contains stage -%}disable-{{ stage }} {% endunless -%}{%- endfor -%}
{%- endcapture -%}

<svg class="lifecycle lifecycle-circle {{ disabled | strip }}" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 320 320" width="320" height="320">
  <title>Sigrid Agentic Software Lifecycle</title>
  <defs>
    <linearGradient id="ramp" gradientUnits="userSpaceOnUse" x1="0" y1="-9.0" x2="0" y2="329.0">
      <stop offset="0" stop-color="#151632"/><stop offset="1" stop-color="#1B64FF"/>
    </linearGradient>
    <!-- clockwise arcs (glyph tops face outward); the bottom arc runs
         counter-clockwise so its label stays upright -->
    <path id="aTop" fill="none" d="M75.28,83.72 A114,114 0 0 1 244.72,83.72"/>
    <path id="aRight" fill="none" d="M236.28,75.28 A114,114 0 0 1 236.28,244.72"/>
    <path id="aLeft" fill="none" d="M83.72,244.72 A114,114 0 0 1 83.72,75.28"/>
    <path id="aBottom" fill="none" d="M62.65,247.66 A131,131 0 0 0 257.35,247.66"/>
    <filter id="soft" x="-30%" y="-30%" width="160%" height="160%">
      <feDropShadow dx="0" dy="3" stdDeviation="5" flood-color="#151632" flood-opacity=".18"/>
    </filter>
  </defs>
  <g filter="url(#soft)">
    <path class="q s-grounding" d="M58.69,52.11 A148.0,148.0 0 0 1 261.31,52.11 L227.09,88.56 A98.0,98.0 0 0 0 92.91,88.56 Z" fill="url(#ramp)"/>
    <path class="q s-plan" d="M267.89,58.69 A148.0,148.0 0 0 1 267.89,261.31 L231.44,227.09 A98.0,98.0 0 0 0 231.44,92.91 Z" fill="url(#ramp)"/>
    <path class="q s-prevent" d="M261.31,267.89 A148.0,148.0 0 0 1 58.69,267.89 L92.91,231.44 A98.0,98.0 0 0 0 227.09,231.44 Z" fill="url(#ramp)"/>
    <path class="q s-improve" d="M52.11,261.31 A148.0,148.0 0 0 1 52.11,58.69 L88.56,92.91 A98.0,98.0 0 0 0 88.56,227.09 Z" fill="#F8C716"/>
  </g>
  <text class="lbl s-grounding" fill="#FFFFFF"><textPath href="#aTop" xlink:href="#aTop" startOffset="50%" text-anchor="middle">Grounding</textPath></text>
  <text class="lbl s-plan" fill="#FFFFFF"><textPath href="#aRight" xlink:href="#aRight" startOffset="50%" text-anchor="middle">Plan</textPath></text>
  <text class="lbl s-prevent" fill="#FFFFFF"><textPath href="#aBottom" xlink:href="#aBottom" startOffset="50%" text-anchor="middle">Prevent</textPath></text>
  <text class="lbl s-improve" fill="#151632"><textPath href="#aLeft" xlink:href="#aLeft" startOffset="50%" text-anchor="middle">Improve</textPath></text>
  <g filter="url(#soft)">
    <circle cx="73.0" cy="73.0" r="17" fill="#FFFFFF"/>
    <circle class="qb s-grounding" cx="73.0" cy="73.0" r="14" fill="#16214E"/>
    <circle cx="247.0" cy="73.0" r="17" fill="#FFFFFF"/>
    <circle class="qb s-plan" cx="247.0" cy="73.0" r="14" fill="#183D98"/>
    <circle cx="247.0" cy="247.0" r="17" fill="#FFFFFF"/>
    <circle class="qb s-prevent" cx="247.0" cy="247.0" r="14" fill="#1A59E3"/>
    <circle cx="73.0" cy="247.0" r="17" fill="#FFFFFF"/>
    <circle class="qb s-improve" cx="73.0" cy="247.0" r="14" fill="#F8C716"/>
  </g>
  <text class="num qn s-grounding" x="73.0" y="76.3" text-anchor="middle" fill="#FFFFFF">1</text>
  <text class="num qn s-plan" x="247.0" y="76.3" text-anchor="middle" fill="#FFFFFF">2</text>
  <text class="num qn s-prevent" x="247.0" y="250.3" text-anchor="middle" fill="#FFFFFF">3</text>
  <text class="num qn s-improve" x="73.0" y="250.3" text-anchor="middle" fill="#151632">4</text>
  <circle cx="160.0" cy="160.0" r="94.0" fill="#FFFFFF"/>
  <circle cx="160.0" cy="160.0" r="84.0" fill="none" stroke="#EBEBEB" stroke-width="1.2" stroke-dasharray="2 6"/>
    <g fill="#151632" transform="translate(106.00,118.00) scale(0.284136) translate(0,413) scale(0.1,-0.1)">
      <path d="M421,4123.8c-72-12-185-68-242-118c-120-105-163-315-95-456c52-106,150-174,401-282c150-64,216-147,199-252c-20-128-160-193-318-147c-88,26-134,78-211,242c-61,128-66,134-94,134c-56,0-61-6-61-79c0-36,5-118,10-181c9-112,10-116,41-142c80-67,267-114,424-105c156,9,261,53,352,150c62,66,98,141,112,237c34,222-85,371-379,480c-177,65-243,116-256,197c-29,183,218,280,376,148c53-44,90-46,131-6c43,44,35,107-19,135C715,4118.8,523,4141.8,421,4123.8z"/>
      <path d="M3629,4120.8c-5-5-194-42-261-51c-45-6-48-8-48-36c0-24,4-29,25-29c44,0,75-21,86-59c5-20,9-93,7-164l-3-127l-100-4c-119-4-186-26-275-91c-200-148-257-443-125-650c62-98,166-164,270-173c68-5,95,5,176,64c26,19,49,34,53,34c3,0,6-23,6-51c0-45,2-50,18-44c32,12,176,43,260,56l83,13l-3,30c-3,28-7,32-45,37c-79,10-73-41-73,640v609h-23C3644,4124.8,3631,4122.8,3629,4120.8z M3369,3559.8c16-8,38-30,50-50c20-35,21-49,21-321v-285l-36-15c-113-47-235,66-265,246c-13,75-5,202,17,277C3193,3538.8,3286,3603.8,3369,3559.8z"/>
      <path d="M1068,3928.8c-31-16-58-61-58-96c0-37,34-90,71-110c74-40,161-8,188,68c13,37,12,44-5,80C1232,3936.8,1135,3965.8,1068,3928.8z"/>
      <path d="M2482,3748.8c-46-23-96-73-139-140c-10-16-12-12-12,29c-1,65,12,67-248-35c-91-35-103-42-103-64c0-16,9-28,28-38c15-8,38-26,52-41l25-27l3-290c2-210,0-294-9-304c-7-9-31-14-60-14h-49v-38v-39h465h465v38v39h-49c-35,0-51,4-55,16c-3,9-6,162-6,340c0,279-2,325-15,330c-8,4-63-13-121-35c-58-23-130-51-160-62c-47-18-54-24-54-47c0-21,8-32,35-46c62-34,66-49,72-245c3-97,1-192-4-211l-9-35l-92-3c-83-2-92-1-102,18c-7,14-10,116-8,318c3,294,3,297,28,347c22,45,29,50,62,53c20,2,50-4,67-12c42-22,107-20,146,4c71,44,83,133,25,192C2622,3784.8,2556,3785.8,2482,3748.8z"/>
      <path d="M970,3256.8c0-312-3-421-12-430c-7-7-31-12-55-12h-43v-40v-40l201,1c110,1,202-1,204-3s-1-22-8-45c-14-55,3-112,48-156l34-33l-50-49c-85-85-126-199-100-278c37-111,224-175,481-164c329,15,541,161,541,374c0,128-79,227-221,275c-58,19-87,22-273,23c-192,1-210,3-235,22c-41,30-41,72,0,115l33,35l101-5c154-7,257,30,344,124c63,68,84,123,84,219c-1,100-26,164-92,227c-95,91-186,123-331,116c-82-4-106-10-162-36c-83-40-149-104-184-178c-65-138-12-317,119-400c25-16,46-32,46-36s-18-17-39-28c-22-11-42-24-46-30c-3-5-33-10-65-10c-48,0-61,4-70,19c-6,12-10,121-10,286c0,302,3,318,69,360c29,18,41,32,41,49c0,22-13,29-122,72c-68,25-138,53-157,60c-18,8-42,14-52,14C971,3674.8,970,3658.8,970,3256.8z M1732,3433.8c68-36,78-307,16-437c-53-112-186-84-224,46c-33,112-8,294,49,364C1609,3451.8,1677,3462.8,1732,3433.8z M1930,2507.8c92-46,117-137,61-225c-106-167-427-225-553-99c-41,42-53,75-44,125c15,78,116,169,233,207C1711,2542.8,1867,2538.8,1930,2507.8z"/>
    </g>
  <text class="tag" x="160.0" y="199.3" text-anchor="middle" fill="#1B64FF">AGENTIC LIFECYCLE</text>
</svg>

