use std::str::FromStr;
use std::path::PathBuf;

use slog::Logger;
use minidom::{Element, Error, ErrorKind};

use utils::parse::{FromElem, assert_root_name, attr_map, child_text, get_child_no_ns, attr_parse};

#[derive(Debug, PartialEq, Eq, Clone, Serialize)]
pub enum FileCategory{
    Doc,
    Header,
    Include,
    Library,
    Object,
    Source,
    SourceC,
    SourceCpp,
    SourceAsm,
    LinkerScript,
    Utility,
    Image,
    Other,
}

impl FromStr for FileCategory {
    type Err = Error;
    fn from_str(from: &str) -> Result<Self, Error> {
        match from {
            "doc" => Ok(FileCategory::Doc),
            "header" => Ok(FileCategory::Header),
            "include" => Ok(FileCategory::Include),
            "library" => Ok(FileCategory::Library),
            "object" => Ok(FileCategory::Object),
            "source" => Ok(FileCategory::Source),
            "sourceC" => Ok(FileCategory::SourceC),
            "sourceCpp" => Ok(FileCategory::SourceCpp),
            "sourceAsm" => Ok(FileCategory::SourceAsm),
            "linkerScript" => Ok(FileCategory::LinkerScript),
            "utility" => Ok(FileCategory::Utility),
            "image" => Ok(FileCategory::Image),
            "other" => Ok(FileCategory::Other),
            unknown => Err(err_msg!("Unknown file catogory {}", unknown)),
        }
    }
}

#[derive(Debug, PartialEq, Eq, Clone, Serialize)]
pub enum FileAttribute{
    Config,
    Template,
}

impl FromStr for FileAttribute {
    type Err = Error;
    fn from_str(from: &str) -> Result<Self, Error> {
        match from {
            "config" => Ok(FileAttribute::Config),
            "template" => Ok(FileAttribute::Template),
            unknown => Err(err_msg!("Unknown file attribute {}", unknown)),
        }
    }
}


#[derive(Debug, Clone, Serialize)]
pub struct FileRef {
    pub path: PathBuf,
    category: FileCategory,
    attr: Option<FileAttribute>,
    pub condition: Option<String>,
    select: Option<String>,
    src: Option<String>,
    version: Option<String>,
}

impl FromElem for FileRef {
    fn from_elem(e: &Element, _: &Logger) -> Result<Self, Error> {
        assert_root_name(e, "file")?;
        Ok(Self {
            path: attr_map(e, "name", "file")?,
            category: attr_parse(e, "category", "file")?,
            attr: attr_parse(e, "attr", "file").ok(),
            condition: attr_map(e, "condition", "file").ok(),
            select: attr_map(e, "select", "file").ok(),
            src: attr_map(e, "src", "file").ok(),
            version: attr_map(e, "version", "file").ok(),
        })
    }
}

#[derive(Debug, Clone)]
pub struct ComponentBuilder {
    pub vendor: Option<String>,
    pub class: Option<String>,
    pub group: Option<String>,
    pub sub_group: Option<String>,
    pub variant: Option<String>,
    pub version: Option<String>,
    pub api_version: Option<String>,
    pub condition: Option<String>,
    pub max_instances: Option<u8>,
    pub is_default: bool,
    pub deprecated: bool,
    pub description: String,
    pub rte_addition: String,
    pub files: Vec<FileRef>,
}

impl FromElem for ComponentBuilder {
    fn from_elem(e: &Element, l: &Logger) -> Result<Self, Error> {
        assert_root_name(e, "component")?;
        let mut l = l.new(o!("in" => "Component"));
        let vendor: Option<String> = attr_map(e, "Cvendor", "component").ok();
        if let Some(v) = vendor.clone() {
            l = l.new(o!("Vendor" => v));
        }
        let class: Option<String> = attr_map(e, "Cclass", "component").ok();
        if let Some(c) = class.clone() {
            l = l.new(o!("Class" => c));
        }
        let group: Option<String> = attr_map(e, "Cgroup", "component").ok();
        if let Some(g) = group.clone() {
            l = l.new(o!("Group" => g));
        }
        let sub_group: Option<String> = attr_map(e, "Csub", "component").ok();
        if let Some(s) = vendor.clone() {
            l = l.new(o!("SubGroup" => s));
        }
        let files = get_child_no_ns(e, "files")
            .map(move |child| {
                FileRef::vec_from_children(child.children(), &l)
            })
            .unwrap_or_default();
        Ok(Self {
            vendor,
            class,
            group,
            sub_group,
            version: attr_map(e, "Cversion", "component").ok(),
            variant: attr_map(e, "Cvariant", "component").ok(),
            api_version: attr_map(e, "Capiversion", "component").ok(),
            condition: attr_map(e, "condition", "component").ok(),
            max_instances: attr_parse(e, "maxInstances", "component").ok(),
            is_default: attr_parse(e, "isDefaultVariant", "component").unwrap_or(true),
            description: child_text(e, "description", "component")?,
            deprecated: child_text(e, "deprecated", "component")
                .map(|s| s.parse().unwrap_or(false))
                .unwrap_or(false),
            rte_addition: child_text(e, "RTE_components_h", "component").unwrap_or_default(),
            files,
        })
    }
}

#[derive(Debug)]
pub struct Bundle {
    name: String,
    class: String,
    version: String,
    vendor: Option<String>,
    description: String,
    doc: String,
    components: Vec<ComponentBuilder>,
}

impl Bundle {
    pub fn into_components(self, l: &Logger) -> Vec<ComponentBuilder> {
        let class = self.class;
        let version = self.version;
        let vendor = self.vendor;
        if self.components.is_empty() {
            let mut l = l.new(o!("in" => "Bundle",
                                 "Class" => class.clone()));
            if let Some(v) = vendor.clone() {
                l = l.new(o!("Vendor" => v));
            }
            warn!(l, "Bundle should not be empty")
        }
        self.components
            .into_iter()
            .map(|comp| {
                ComponentBuilder {
                    class: comp.class.or_else(|| Some(class.clone())),
                    version: comp.version.or_else(|| Some(version.clone())),
                    vendor: comp.vendor.or_else(|| vendor.clone()),
                    ..comp
                }
            })
            .collect()
    }
}

impl FromElem for Bundle {
    fn from_elem(e: &Element, l: &Logger) -> Result<Self, Error> {
        assert_root_name(e, "bundle")?;
        let name: String = attr_map(e, "Cbundle", "bundle")?;
        let class: String = attr_map(e, "Cclass", "bundle")?;
        let version: String = attr_map(e, "Cversion", "bundle")?;
        let l = l.new(o!("Bundle" => name.clone(),
                         "Class" => class.clone(),
                         "Version" => version.clone()));
        let components = e.children()
            .filter_map(move |chld| if chld.name() == "component" {
                ComponentBuilder::from_elem(chld, &l).ok()
            } else {
                None
            })
            .collect();
        Ok(Self {
            name,
            class,
            version,
            vendor: attr_map(e, "Cvendor", "bundle").ok(),
            description: child_text(e, "description", "bundle")?,
            doc: child_text(e, "doc", "bundle")?,
            components,
        })
    }
}

fn child_to_component_iter(
    e: &Element,
    l: &Logger,
) -> Result<Box<dyn Iterator<Item = ComponentBuilder>>, Error> {
    match e.name() {
        "bundle" => {
            let bundle = Bundle::from_elem(e, l)?;
            Ok(Box::new(bundle.into_components(l).into_iter()))
        }
        "component" => {
            let component = ComponentBuilder::from_elem(e, l)?;
            Ok(Box::new(Some(component).into_iter()))
        }
        _ => Err(Error::from_kind(ErrorKind::Msg(String::from(format!(
            "element of name {} is not allowed as a descendant of components",
            e.name()
        ))))),
    }
}

#[derive(Default)]
pub struct ComponentBuilders(pub(crate) Vec<ComponentBuilder>);

impl FromElem for ComponentBuilders {
    fn from_elem(e: &Element, l: &Logger) -> Result<Self, Error> {
        assert_root_name(e, "components")?;
        Ok(ComponentBuilders(
            e.children()
                .flat_map(move |c| match child_to_component_iter(c, l) {
                    Ok(iter) => iter,
                    Err(e) => {
                        error!(l, "when trying to parse component: {}", e);
                        Box::new(None.into_iter())
                    }
                })
                .collect(),
        ))
    }
}
