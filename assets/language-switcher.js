(function () {
  "use strict";

  const storeKey = "stemhub-amc-language";
  const supported = new Set(["zh", "en"]);
  const dictionary = window.STEMHUB_I18N;
  if (!dictionary) return;

  function queryLanguage() {
    const requested = new URLSearchParams(window.location.search).get("lang");
    return supported.has(requested) ? requested : "";
  }

  function currentLanguage() {
    return queryLanguage() || localStorage.getItem(storeKey) || "zh";
  }

  function translate(key, values) {
    const language = currentLanguage();
    const template = dictionary.messages[language][key] || dictionary.messages.en[key] || key;
    return String(template).replace(/\{(\w+)\}/g, (_, name) => values && values[name] != null ? values[name] : `{${name}}`);
  }

  function taxonomyLabel(group, raw) {
    if (currentLanguage() === "zh") return raw;
    return dictionary.taxonomy[group] && dictionary.taxonomy[group][raw] || raw;
  }

  function yearLabel(raw) {
    if (raw === "2021 Spring") return translate("year.spring");
    if (raw === "2021 Fall") return translate("year.fall");
    return raw;
  }

  function formLabel(raw) {
    return raw === "A" || raw === "B" ? translate(`form.${raw}`) : raw;
  }

  function isChinese(value) {
    return /[\u3400-\u9fff]/.test(String(value || ""));
  }

  function rememberRaw(element) {
    if (!element.dataset.i18nRaw) element.dataset.i18nRaw = element.textContent.trim();
    return element.dataset.i18nRaw;
  }

  function localizeBadge(element) {
    const raw = rememberRaw(element);
    let label = raw;
    if (/^Problem\s+(\d+)$/i.test(raw) || /^题目\s*(\d+)$/.test(raw)) {
      const number = raw.match(/\d+/)[0];
      label = translate("detail.problem", { number });
    } else if (dictionary.taxonomy.major[raw]) {
      label = taxonomyLabel("major", raw);
    } else if (dictionary.taxonomy.minor[raw]) {
      label = taxonomyLabel("minor", raw);
    } else if (dictionary.taxonomy.tags[raw]) {
      label = taxonomyLabel("tags", raw);
    }
    element.textContent = label;
  }

  function localizeCounts() {
    document.querySelectorAll(".year-card span").forEach((element) => {
      const raw = rememberRaw(element);
      const match = raw.match(/^(\d+)\s*(?:题|problems?)$/i);
      if (match) element.textContent = currentLanguage() === "zh" ? `${match[1]} 题` : `${match[1]} problems`;
    });
  }

  function setText(element, value) {
    if (element && element.textContent !== value) element.textContent = value;
  }

  function directTextNode(element) {
    return Array.from(element.childNodes).find((node) => node.nodeType === Node.TEXT_NODE && node.nodeValue.trim());
  }

  function localizedRawValue(raw) {
    if (raw === "A卷" || raw === "A 卷" || raw === "Form A") return formLabel("A");
    if (raw === "B卷" || raw === "B 卷" || raw === "Form B") return formLabel("B");
    if (raw === "全部年份" || raw === "All years") return translate("filter.allYears");
    if (raw === "全部卷别" || raw === "All forms") return translate("filter.allForms");
    if (raw === "全部一级分类" || raw === "All major categories") return translate("filter.allMajor");
    if (raw === "全部二级分类" || raw === "All minor categories") return translate("filter.allMinor");
    if (raw === "无关键词" || raw === "No keyword") return translate("filter.noKeyword");
    if (/^(\d+)\s*(?:题|problems?)$/i.test(raw)) {
      const count = raw.match(/\d+/)[0];
      return currentLanguage() === "zh" ? `${count} 题` : `${count} problems`;
    }
    if (dictionary.taxonomy.major[raw]) return taxonomyLabel("major", raw);
    if (dictionary.taxonomy.minor[raw]) return taxonomyLabel("minor", raw);
    if (dictionary.taxonomy.tags[raw]) return taxonomyLabel("tags", raw);
    return raw;
  }

  function localizeOverviewPage() {
    const isOverview = document.querySelector("#yearFilter") && document.querySelector("#cards");
    if (!isOverview) return;

    const nav = document.querySelector(".site-nav");
    if (nav) nav.setAttribute("aria-label", translate("nav.site"));
    document.querySelectorAll(".site-links a").forEach((link) => {
      const href = link.getAttribute("href") || "";
      if (href === "../" || href === "/STEMHUB_AMC/") setText(link, translate("nav.home"));
      if (href === "#downloads") setText(link, translate("nav.downloads"));
    });

    const title = document.querySelector("header h1");
    const isAmc10 = document.querySelector("#statTotal")?.textContent.trim() === "1150" || /AMC 10/.test(title?.textContent || "");
    if (title) setText(title, translate(isAmc10 ? "overview.amc10Title" : "overview.amc12Title"));
    const subtitle = document.querySelector("header p");
    if (subtitle) setText(subtitle, translate(isAmc10 ? "overview.amc10Subtitle" : "overview.amc12Subtitle"));

    const statKeys = ["overview.currentProblems", "overview.currentYears", "overview.formACount", "overview.formBCount"];
    document.querySelectorAll(".stats > .stat > span").forEach((element, index) => setText(element, translate(statKeys[index])));
    const download = document.querySelector("#downloads");
    if (download) {
      download.setAttribute("aria-label", translate("nav.downloads"));
      const downloadTitle = download.querySelector(".download-title");
      const downloadSubtitle = download.querySelector(".muted");
      setText(downloadTitle, translate("overview.downloadTitle"));
      setText(downloadSubtitle, translate("overview.downloadSubtitle"));
      download.querySelectorAll(".download-links a").forEach((link) => {
        const href = link.getAttribute("href") || "";
        const key = href.includes("all_problems") ? "overview.allProblemsCsv"
          : href.includes("taxonomy") ? "overview.taxonomy"
          : href.includes("validation") ? "overview.validation"
          : href.includes("progress") ? "overview.progress"
          : href.includes("latex_build") ? "overview.latexReport"
          : href.includes("latex/") ? "overview.latexBook" : "";
        if (key) setText(link, translate(key));
      });
    }

    document.querySelectorAll(".year-card").forEach((button) => {
      const year = button.dataset.year || "";
      const strong = button.querySelector("strong");
      if (strong) setText(strong, year ? yearLabel(year) : translate("filter.allYears"));
    });
    localizeCounts();

    const headings = Array.from(document.querySelectorAll(".panel > h2, .filter-header > h2"));
    headings.forEach((heading) => {
      if (heading.id === "majorPanelTitle") return;
      const raw = rememberRaw(heading);
      if (raw === "年份") setText(heading, translate("overview.years"));
      else if (raw === "一级分类") setText(heading, translate("overview.majorCategory"));
      else if (raw === "筛选题目") setText(heading, translate("overview.filterProblems"));
    });
    const clear = document.querySelector("#clearFilters");
    if (clear) setText(clear, translate("filter.clear"));

    const labels = {
      yearFilter: "filter.year", formFilter: "filter.form", majorFilter: "filter.major", minorFilter: "filter.minor", searchInput: "filter.search"
    };
    Object.entries(labels).forEach(([id, key]) => {
      const control = document.getElementById(id);
      const label = control?.closest("label");
      const textNode = label && directTextNode(label);
      if (textNode) textNode.nodeValue = translate(key);
    });
    const search = document.getElementById("searchInput");
    if (search) search.setAttribute("placeholder", translate("filter.searchPlaceholder"));
    const selectRules = {
      yearFilter: (option) => option.value ? yearLabel(option.value) : translate("filter.allYears"),
      formFilter: (option) => option.value ? formLabel(option.value) : translate("filter.allForms"),
      majorFilter: (option) => option.value ? taxonomyLabel("major", option.value) : translate("filter.allMajor"),
      minorFilter: (option) => option.value ? taxonomyLabel("minor", option.value) : translate("filter.allMinor")
    };
    Object.entries(selectRules).forEach(([id, labelFor]) => {
      document.querySelectorAll(`#${id} option`).forEach((option) => setText(option, labelFor(option)));
    });

    document.querySelectorAll("#filterSummary .summary-chip").forEach((chip) => {
      const label = chip.querySelector("strong");
      const keyByRaw = { "年份":"filter.year", "卷别":"filter.form", "一级分类":"filter.major", "二级分类":"filter.minor", "关键词":"filter.search", "结果":"filter.results" };
      if (label) {
        const rawLabel = rememberRaw(label);
        if (keyByRaw[rawLabel]) setText(label, translate(keyByRaw[rawLabel]));
      }
      const value = directTextNode(chip);
      if (value) value.nodeValue = localizedRawValue(value.nodeValue.trim());
    });

    const result = document.querySelector("#resultCount");
    if (result) {
      const counts = result.textContent.match(/(\d+)/g);
      if (counts?.length >= 2) setText(result, translate("overview.resultCount", { shown: counts[0], total: counts[1] }));
    }

    const majorFilter = document.getElementById("majorFilter");
    const yearFilter = document.getElementById("yearFilter");
    const panelTitle = document.getElementById("majorPanelTitle");
    const compareHeaders = document.querySelectorAll(".compare-head span");
    const formACount = compareHeaders[1]?.textContent.match(/\d+/)?.[0] || "0";
    const formBCount = compareHeaders[2]?.textContent.match(/\d+/)?.[0] || "0";
    if (panelTitle) {
      const scope = yearFilter?.value ? yearLabel(yearFilter.value) : translate("filter.allYears");
      const key = majorFilter?.value ? "overview.minorCompare" : "overview.majorCompare";
      setText(panelTitle, translate(key, { major: taxonomyLabel("major", majorFilter?.value || ""), scope, a: formACount, b: formBCount }));
    }
    compareHeaders.forEach((element, index) => {
      const keys = [majorFilter?.value ? "overview.compareMinor" : "overview.compareCategory", "overview.compareFormA", "overview.compareFormB", "overview.partRange"];
      setText(element, index === 1 ? translate(keys[index], { total: formACount }) : index === 2 ? translate(keys[index], { total: formBCount }) : translate(keys[index]));
    });
    document.querySelectorAll(".bar-row").forEach((row) => {
      const category = row.querySelector(":scope > span");
      if (category) {
        const raw = rememberRaw(category);
        setText(category, majorFilter?.value ? taxonomyLabel("minor", raw) : taxonomyLabel("major", raw));
      }
      row.querySelectorAll(".compare-meta").forEach((meta) => {
        const raw = rememberRaw(meta);
        const count = raw.match(/^\s*(\d+)/)?.[1];
        const percentage = raw.match(/(\d+(?:\.\d+)?%)/)?.[1];
        if (count && percentage) setText(meta, currentLanguage() === "zh" ? `${count}题 / ${percentage}` : `${count} problems / ${percentage}`);
      });
      const partCell = row.querySelector(".part-cell");
      if (partCell) partCell.setAttribute("aria-label", translate("part.aria"));
      row.querySelectorAll(".part-pill").forEach((pill, index) => {
        const raw = rememberRaw(pill);
        const count = raw.match(/\d+/)?.[0] || "0";
        const percentage = raw.match(/(\d+(?:\.\d+)?%)/)?.[1] || "0.0%";
        setText(pill, `${translate(`part.${index + 1}`)} ${count} / ${percentage}`);
      });
    });

    document.querySelectorAll("#cards .badge").forEach(localizeBadge);
    document.querySelectorAll("#cards .idea").forEach((idea) => {
      const raw = rememberRaw(idea);
      if (currentLanguage() === "en" && isChinese(raw)) idea.dataset.languageNote = translate("content.chineseNote");
      else delete idea.dataset.languageNote;
      const note = idea.querySelector("strong");
      if (note) setText(note, translate("overview.notes"));
    });
    document.querySelectorAll("#cards .detail-cta").forEach((element) => setText(element, translate("overview.viewDetails")));
    document.querySelectorAll("#cards .problem-link").forEach((link) => {
      const source = link.querySelector(".source")?.textContent || "";
      link.setAttribute("aria-label", currentLanguage() === "zh" ? `查看 ${source} 的详情` : `View details for ${source}`);
    });
  }

  function localizeDetailPage() {
    const isDetail = /\/problems\//.test(window.location.pathname);
    if (!isDetail) return;
    const nav = document.querySelector(".site-nav");
    if (nav) nav.setAttribute("aria-label", currentLanguage() === "zh" ? "全站导航" : "Site navigation");

    document.querySelectorAll(".site-links a").forEach((link) => {
      const href = link.getAttribute("href") || "";
      if (href.includes("amc10/")) link.textContent = "AMC 10";
      else if (href.includes("amc12/")) link.textContent = "AMC 12";
      else if (href === "../../../" || href === "/STEMHUB_AMC/") link.textContent = translate("nav.home");
      else if (href === "../../") link.textContent = translate("nav.backToOverview");
    });

    document.querySelectorAll(".back").forEach((link) => {
      const raw = rememberRaw(link);
      const contest = raw.includes("AMC 10") ? "AMC 10" : "AMC 12";
      link.textContent = translate("detail.backToOverview", { contest });
    });

    const sectionKeys = {
      "Problem Statement": "detail.problemStatement", "题目": "detail.problemStatement",
      "Choices": "detail.choices", "选项": "detail.choices",
      "Answer": "detail.answer", "答案": "detail.answer",
      "Solution": "detail.solution", "解答": "detail.solution",
      "Key Idea": "detail.keyIdea", "核心思路": "detail.keyIdea",
      "Notes": "detail.notes", "备注": "detail.notes",
      "Reference": "detail.reference", "参考": "detail.reference"
    };
    document.querySelectorAll(".section h2").forEach((heading) => {
      const raw = rememberRaw(heading);
      if (sectionKeys[raw]) heading.textContent = translate(sectionKeys[raw]);
    });

    document.querySelectorAll(".step h3").forEach((heading) => {
      const raw = rememberRaw(heading);
      const match = raw.match(/^(?:Step|步骤)\s*(\d+)\s*:\s*(.*)$/i);
      if (match) heading.textContent = `${translate("detail.step", { number: match[1] })}: ${match[2]}`;
    });

    document.querySelectorAll(".badge").forEach(localizeBadge);
    const metadata = document.querySelector(".meta");
    if (metadata) metadata.setAttribute("aria-label", translate("detail.metadata"));

    document.querySelectorAll(".references p").forEach((paragraph) => {
      const links = paragraph.querySelectorAll("a");
      if (links.length < 2) return;
      const answerHref = links[0].getAttribute("href");
      const problemHref = links[1].getAttribute("href");
      paragraph.innerHTML = `${translate("detail.answerVerified")} <a href="${answerHref}">AoPS Answer Key</a>. ${translate("detail.relatedPage")}: <a href="${problemHref}">AoPS problem page</a>.`;
    });
  }

  function localizeStaticText() {
    document.documentElement.lang = currentLanguage() === "zh" ? "zh-CN" : "en";
    document.body.dataset.language = currentLanguage();
    document.querySelectorAll("[data-i18n]").forEach((element) => {
      element.textContent = translate(element.dataset.i18n);
    });
    document.querySelectorAll("[data-i18n-placeholder]").forEach((element) => {
      element.setAttribute("placeholder", translate(element.dataset.i18nPlaceholder));
    });
    document.querySelectorAll("[data-i18n-aria-label]").forEach((element) => {
      element.setAttribute("aria-label", translate(element.dataset.i18nAriaLabel));
    });
    document.querySelectorAll("[data-i18n-title]").forEach((element) => {
      document.title = translate(element.dataset.i18nTitle);
    });
    localizeCounts();
    localizeDetailPage();
    localizeOverviewPage();
  }

  function ensureSwitcher() {
    const nav = document.querySelector(".site-nav");
    if (!nav) return;
    const links = nav.querySelector(":scope > .site-links");
    if (!links) return;
    let actions = nav.querySelector(":scope > .site-nav-actions");
    if (!actions) {
      actions = document.createElement("div");
      actions.className = "site-nav-actions";
      nav.insertBefore(actions, links);
      actions.appendChild(links);
    }
    let switcher = actions.querySelector(".language-switcher");
    if (!switcher) {
      switcher = document.createElement("div");
      switcher.className = "language-switcher";
      switcher.setAttribute("role", "group");
      switcher.setAttribute("aria-label", translate("nav.language"));
      switcher.innerHTML = '<button type="button" data-language="zh">中文</button><button type="button" data-language="en">EN</button>';
      actions.appendChild(switcher);
      switcher.addEventListener("click", (event) => {
        const button = event.target.closest("button[data-language]");
        if (button) setLanguage(button.dataset.language);
      });
    }
    switcher.setAttribute("aria-label", translate("nav.language"));
    switcher.querySelectorAll("button[data-language]").forEach((button) => {
      button.setAttribute("aria-pressed", String(button.dataset.language === currentLanguage()));
    });
  }

  function setLanguage(language) {
    if (!supported.has(language)) return;
    localStorage.setItem(storeKey, language);
    const url = new URL(window.location.href);
    url.searchParams.set("lang", language);
    window.history.replaceState({}, "", url);
    ensureSwitcher();
    localizeStaticText();
    ensureSwitcher();
    document.dispatchEvent(new CustomEvent("stemhub:languagechange", { detail: { language } }));
  }

  function start() {
    const requested = queryLanguage();
    if (requested) localStorage.setItem(storeKey, requested);
    ensureSwitcher();
    localizeStaticText();
    ensureSwitcher();
    const overviewRoot = document.querySelector("#cards")?.closest("main");
    if (overviewRoot && !overviewRoot.dataset.i18nObserver) {
      overviewRoot.dataset.i18nObserver = "true";
      let scheduled = false;
      new MutationObserver(() => {
        if (scheduled) return;
        scheduled = true;
        window.requestAnimationFrame(() => {
          scheduled = false;
          localizeOverviewPage();
        });
      }).observe(overviewRoot, { childList: true, subtree: true });
    }
    document.dispatchEvent(new CustomEvent("stemhub:languagechange", { detail: { language: currentLanguage() } }));
  }

  window.STEMHUB_LANGUAGE = {
    get: currentLanguage,
    set: setLanguage,
    t: translate,
    major: (value) => taxonomyLabel("major", value),
    minor: (value) => taxonomyLabel("minor", value),
    tag: (value) => taxonomyLabel("tags", value),
    year: yearLabel,
    form: formLabel,
    isChinese
  };

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start, { once: true });
  else start();
})();
