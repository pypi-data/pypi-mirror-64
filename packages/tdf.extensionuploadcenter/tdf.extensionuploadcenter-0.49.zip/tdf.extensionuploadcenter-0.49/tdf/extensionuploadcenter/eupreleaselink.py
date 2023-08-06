# -*- coding: utf-8 -*-
from tdf.extensionuploadcenter import _
from plone.app.textfield import RichText
from plone.supermodel import model
from zope import schema
from plone.dexterity.browser.view import DefaultView
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.interface import directlyProvides
from plone.indexer.decorator import indexer

from zope.security import checkPermission
from zope.interface import invariant, Invalid
from Acquisition import aq_inner, aq_parent
from z3c.form.browser.checkbox import CheckBoxFieldWidget

from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory
from Products.validation import V_REQUIRED
from plone import api
from z3c.form import validator
import re
from plone.supermodel.directives import primary
from plone.autoform import directives


def vocabAvailLicenses(context):
    """ pick up licenses list from parent """

    license_list = getattr(context.__parent__, 'available_licenses', [])
    terms = []
    for value in license_list:
        terms.append(SimpleTerm(value, token=value.encode('unicode_escape'),
                                title=value))
    return SimpleVocabulary(terms)


directlyProvides(vocabAvailLicenses, IContextSourceBinder)


def vocabAvailVersions(context):
    """ pick up the program versions list from parent """

    versions_list = getattr(context.__parent__, 'available_versions', [])
    terms = []
    for value in versions_list:
        terms.append(SimpleTerm(value, token=value.encode('unicode_escape'),
                                title=value))
    return SimpleVocabulary(terms)


directlyProvides(vocabAvailVersions, IContextSourceBinder)


def vocabAvailPlatforms(context):
    """ pick up the list of platforms from parent """

    platforms_list = getattr(context.__parent__, 'available_platforms', [])
    terms = []
    for value in platforms_list:
        terms.append(SimpleTerm(value, token=value.encode('unicode_escape'),
                                title=value))
    return SimpleVocabulary(terms)


directlyProvides(vocabAvailPlatforms, IContextSourceBinder)

yesnochoice = SimpleVocabulary(
    [SimpleTerm(value=0, title=_(u'No')),
     SimpleTerm(value=1, title=_(u'Yes')), ]
)


@provider(IContextAwareDefaultFactory)
def getContainerTitle(self):
    return self.aq_inner.title


@provider(IContextAwareDefaultFactory)
def contactinfoDefault(context):
    return context.contactAddress


@provider(IContextAwareDefaultFactory)
def legal_declaration_title(context):
    context = context.aq_inner.aq_parent
    return context.title_legaldisclaimer


@provider(IContextAwareDefaultFactory)
def legal_declaration_text(context):
    context = context.aq_inner.aq_parent
    return context.legal_disclaimer


@provider(IContextAwareDefaultFactory)
def allowedextensionfileextensions(context):
    context = context.aq_inner.aq_parent
    return context.allowed_extensionfileextension.replace("|", ", ")


def validatelinkedextensionfileextension(value):
    catalog = api.portal.get_tool(name='portal_catalog')
    result = catalog.uniqueValuesFor('allowedeupextensionfileextensions')
    pattern = r'^.*\.({0})'.format(result[0])
    matches = re.compile(pattern, re.IGNORECASE).match
    if not matches(value):
        raise Invalid(
            u'You could only link to a file with an allowed extension file '
            u'extension. Please try again with to link to a file with the '
            u'correct template file extension.')
    return True


class AcceptLegalDeclaration(Invalid):
    __doc__ = _(u"It is necessary that you accept the Legal Declaration")


class IEUpReleaseLink(model.Schema):
    directives.mode(information="display")
    information = schema.Text(
        title=_(u"Information"),
        description=_(u"This Dialog to create a new linked release consists "
                      u"of different register. Please go through this "
                      u"register and fill in the appropriate data for your "
                      u"linked release. This register 'Default' provide "
                      u"fields for general information of your linked "
                      u"release. The next register 'compatibility is the "
                      u"place to submit information about the versions with "
                      u"which your linked release file(s) is / are "
                      u"compatible. The next register asks for some legal "
                      u"informations. The next register 'Linked File' "
                      u"provide a field to link your release file. The "
                      u"further register are optional. There is the "
                      u"opportunity to link further release files "
                      u"(for different platforms).")
    )

    directives.mode(projecttitle='hidden')
    projecttitle = schema.TextLine(
        title=_(u"The Computed Project Title"),
        description=_(u"The release title will be computed from the parent "
                      u"project title."),
        defaultFactory=getContainerTitle
    )

    releasenumber = schema.TextLine(
        title=_(u"Release Number"),
        description=_(u"Release Number (up to twelf chars)"),
        default=_(u"1.0"),
        max_length=12
    )

    description = schema.Text(
        title=_(u"Release Summary"),
    )

    primary('details')
    details = RichText(
        title=_(u"Full Release Description"),
        required=False
    )

    primary('changelog')
    changelog = RichText(
        title=_(u"Changelog"),
        description=_(u"A detailed log of what has changed since the "
                      u"previous release."),
        required=False,
    )

    model.fieldset('compatibility',
                   label=u"Compatibility",
                   fields=['compatibility_choice'])

    model.fieldset('legal',
                   label=u"Legal",
                   fields=['licenses_choice', 'title_declaration_legal',
                           'declaration_legal', 'accept_legal_declaration',
                           'source_code_inside', 'link_to_source'])

    directives.widget(licenses_choice=CheckBoxFieldWidget)
    licenses_choice = schema.List(
        title=_(u'License of the uploaded file'),
        description=_(u"Please mark one or more licenses you publish your "
                      u"release."),
        value_type=schema.Choice(source=vocabAvailLicenses),
        required=True,
    )

    directives.widget(compatibility_choice=CheckBoxFieldWidget)
    compatibility_choice = schema.List(
        title=_(u"Compatible with versions of LibreOffice"),
        description=_(u"Please mark one or more program versions with which "
                      u"this release is compatible with."),
        value_type=schema.Choice(source=vocabAvailVersions),
        required=True,
    )

    directives.mode(title_declaration_legal='display')
    title_declaration_legal = schema.TextLine(
        title=_(u""),
        required=False,
        defaultFactory=legal_declaration_title
    )

    directives.mode(declaration_legal='display')
    declaration_legal = schema.Text(
        title=_(u""),
        required=False,
        defaultFactory=legal_declaration_text
    )

    accept_legal_declaration = schema.Bool(
        title=_(u"Accept the above legal disclaimer"),
        description=_(u"Please declare that you accept the above legal "
                      u"disclaimer."),
        required=True
    )

    contact_address2 = schema.TextLine(
        title=_(u"Contact email-address"),
        description=_(u"Contact email-address for the project."),
        required=False,
        defaultFactory=contactinfoDefault
    )

    source_code_inside = schema.Choice(
        title=_(u"Is the source code inside the extension?"),
        vocabulary=yesnochoice,
        required=True
    )

    link_to_source = schema.URI(
        title=_(u"Please fill in the Link (URL) to the Source Code."),
        required=False
    )

    model.fieldset('linked_file',
                   label='Linked File',
                   fields=['euplinkedfileextension',
                           'link_to_file',
                           'external_file_size',
                           'platform_choice',
                           'information_further_file_uploads'])

    directives.mode(euplinkedfileextension='display')
    euplinkedfileextension = schema.TextLine(
        title=_(u'The following file extensions are allowed for linked '
                u'files (upper case and lower case and mix of '
                u'both):'),
        defaultFactory=allowedextensionfileextensions,
    )

    link_to_file = schema.URI(
        title=_(u"The Link to the file of the release"),
        description=_(u"Please insert a link to your extension file."),
        required=True,
        constraint=validatelinkedextensionfileextension
    )

    external_file_size = schema.Float(
        title=_(u"The size of the external hosted file"),
        description=_(
            u"Please fill in the size in kilobyte of the external hosted "
            u"file (e.g. 633, if the size is 633 kb)"),
        required=False
    )

    directives.widget(platform_choice=CheckBoxFieldWidget)
    platform_choice = schema.List(
        title=_(u"First linked file is compatible with the Platform(s)"),
        description=_(u"Please mark one or more platforms with which the "
                      u"uploaded file is compatible."),
        value_type=schema.Choice(source=vocabAvailPlatforms),
        required=True,
    )

    directives.mode(information_further_file_uploads='display')
    primary('information_further_file_uploads')
    information_further_file_uploads = RichText(
        title=_(u"Further linked files for this Release"),
        description=_(
            u"If you want to link more files for this release, e.g. because "
            u"there are files for other operating systems, you'll find the "
            u"fields to link this files on the next registers, e.g. "
            u"'Second linked file' "
            u"for this Release'."),
        required=False
    )

    model.fieldset('fieldset1',
                   label=_(u"Second linked file"),
                   fields=['euplinkedfileextension1',
                           'link_to_file1',
                           'external_file_size1',
                           'platform_choice1']
                   )

    model.fieldset('fieldset2',
                   label=_(u"Third linked file"),
                   fields=['euplinkedfileextension2',
                           'link_to_file2',
                           'external_file_size2',
                           'platform_choice2']
                   )

    model.fieldset('fieldset3',
                   label=_(u"Fourth linked file"),
                   fields=['euplinkedfileextension3',
                           'link_to_file3',
                           'external_file_size3',
                           'platform_choice3']
                   )

    model.fieldset('fieldset4',
                   label=_(u"Fifth linked file"),
                   fields=['euplinkedfileextension4',
                           'link_to_file4',
                           'external_file_size4',
                           'platform_choice4']
                   )

    model.fieldset('fieldset5',
                   label=_(u"Sixth linked file"),
                   fields=['euplinkedfileextension5',
                           'link_to_file5',
                           'external_file_size5',
                           'platform_choice5']
                   )

    directives.mode(euplinkedfileextension1='display')
    euplinkedfileextension1 = schema.TextLine(
        title=_(u'The following file extensions are allowed for linked '
                u'files (upper case and lower case and mix of '
                u'both):'),
        defaultFactory=allowedextensionfileextensions,
    )

    link_to_file1 = schema.URI(
        title=_(u"The Link to the file of the release"),
        description=_(u"Please insert a link to your extension file."),
        required=False,
        constraint=validatelinkedextensionfileextension
    )

    external_file_size1 = schema.Float(
        title=_(u"The size of the external hosted file"),
        description=_(u"Please fill in the size in kilobyte of the external "
                      u"hosted file (e.g. 633, if the size is 633 kb)"),
        required=False
    )

    directives.widget(platform_choice1=CheckBoxFieldWidget)
    platform_choice1 = schema.List(
        title=_(u"Second linked file is compatible with the Platform(s)"),
        description=_(u"Please mark one or more platforms with which the "
                      u"linked file is compatible."),
        value_type=schema.Choice(source=vocabAvailPlatforms),
        required=True,
    )

    directives.mode(euplinkedfileextension2='display')
    euplinkedfileextension2 = schema.TextLine(
        title=_(u'The following file extensions are allowed for linked '
                u'files (upper case and lower case and mix of '
                u'both):'),
        defaultFactory=allowedextensionfileextensions,
    )

    link_to_file2 = schema.URI(
        title=_(u"The Link to the file of the release"),
        description=_(u"Please insert a link to your extension file."),
        required=False,
        constraint=validatelinkedextensionfileextension
    )

    external_file_size2 = schema.Float(
        title=_(u"The size of the external hosted file"),
        description=_(u"Please fill in the size in kilobyte of the external "
                      u"hosted file (e.g. 633, if the size is 633 kb)"),
        required=False
    )

    directives.widget(platform_choice2=CheckBoxFieldWidget)
    platform_choice2 = schema.List(
        title=_(u"Third linked file is compatible with the Platform(s)"),
        description=_(u"Please mark one or more platforms with which the "
                      u"linked file is compatible."),
        value_type=schema.Choice(source=vocabAvailPlatforms),
        required=True
    )

    directives.mode(euplinkedfileextension3='display')
    euplinkedfileextension3 = schema.TextLine(
        title=_(u'The following file extensions are allowed for linked '
                u'files (upper case and lower case and mix of '
                u'both):'),
        defaultFactory=allowedextensionfileextensions,
    )

    link_to_file3 = schema.URI(
        title=_(u"The Link to the file of the release"),
        description=_(u"Please insert a link to your extension file."),
        required=False,
        constraint=validatelinkedextensionfileextension
    )

    external_file_size3 = schema.Float(
        title=_(u"The size of the external hosted file"),
        description=_(u"Please fill in the size in kilobyte of the external "
                      u"hosted file (e.g. 633, if the size is 633 kb)"),
        required=False
    )

    directives.widget(platform_choice3=CheckBoxFieldWidget)
    platform_choice3 = schema.List(
        title=_(u"Fourth linked file is compatible with the Platform(s)"),
        description=_(u"Please mark one or more platforms with which the "
                      u"linked file is compatible."),
        value_type=schema.Choice(source=vocabAvailPlatforms),
        required=True,
    )

    directives.mode(euplinkedfileextension4='display')
    euplinkedfileextension4 = schema.TextLine(
        title=_(u'The following file extensions are allowed for linked '
                u'files (upper case and lower case and mix of '
                u'both):'),
        defaultFactory=allowedextensionfileextensions,
    )

    link_to_file4 = schema.URI(
        title=_(u"The Link to the file of the release"),
        description=_(u"Please insert a link to your extension file."),
        required=False,
        constraint=validatelinkedextensionfileextension
    )

    external_file_size4 = schema.Float(
        title=_(u"The size of the external hosted file"),
        description=_(u"Please fill in the size in kilobyte of the external "
                      u"hosted file (e.g. 633, if the size is 633 kb)"),
        required=False
    )

    directives.widget(platform_choice4=CheckBoxFieldWidget)
    platform_choice4 = schema.List(
        title=_(u"Fifth linked file is compatible with the Platform(s)"),
        description=_(u"Please mark one or more platforms with which the "
                      u"linked file is compatible."),
        value_type=schema.Choice(source=vocabAvailPlatforms),
        required=True,
    )

    directives.mode(euplinkedfileextension5='display')
    euplinkedfileextension5 = schema.TextLine(
        title=_(u'The following file extensions are allowed for linked '
                u'files (upper case and lower case and mix of '
                u'both):'),
        defaultFactory=allowedextensionfileextensions,
    )

    link_to_file5 = schema.URI(
        title=_(u"The Link to the file of the release"),
        description=_(u"Please insert a link to your extension file."),
        required=False,
        constraint=validatelinkedextensionfileextension
    )

    external_file_size5 = schema.Float(
        title=_(u"The size of the external hosted file"),
        description=_(u"Please fill in the size in kilobyte of the external "
                      u"hosted file (e.g. 633, if the size is 633 kb)"),
        required=False
    )

    directives.widget(platform_choice5=CheckBoxFieldWidget)
    platform_choice5 = schema.List(
        title=_(u"Sixth linked file is compatible with the Platform(s)"),
        description=_(u"Please mark one or more platforms with which the "
                      u"linked file is compatible."),
        value_type=schema.Choice(source=vocabAvailPlatforms),
        required=True,
    )

    @invariant
    def licensenotchoosen(value):
        if not value.licenses_choice:
            raise Invalid(_(u"Please choose a license for your release."))

    @invariant
    def compatibilitynotchoosen(data):
        if not data.compatibility_choice:
            raise Invalid(_(u"Please choose one or more compatible product "
                            u"versions for your release."))

    @invariant
    def legaldeclarationaccepted(data):
        if data.accept_legal_declaration is not True:
            raise AcceptLegalDeclaration(_(u"Please accept the Legal "
                                           u"Declaration about your Release "
                                           u"and your linked File"))

    @invariant
    def testingvalue(data):
        if data.source_code_inside is not 1 and data.link_to_source is None:
            raise Invalid(_(u"You answered the question, whether the source "
                            u"code is inside your extension with no "
                            u"(default answer). If this is the correct "
                            u"answer, please fill in the Link (URL) "
                            u"to the Source Code."))

    @invariant
    def noOSChosen(data):
        if data.link_to_file is not None and data.platform_choice == []:
            raise Invalid(_(u"Please choose a compatible platform for the "
                            u"linked file."))


@indexer(IEUpReleaseLink)
def release_number(context, **kw):
    return context.releasenumber


def notifyExtensionHubReleaseLinkAdd(self, event):
    state = api.content.get_state(self)
    releasemessagereceipient = self.releaseAllert
    catalog = api.portal.get_tool(name='portal_catalog')
    results = catalog(Title=self.title)
    for brain in results:
        url = brain.getURL()

        category = list(self.category_choice)
        compatibility = list(self.compatibility_choice)
        licenses = list(self.licenses_choice)
        pf_list = \
            list(self.platform_choice) + list(self.platform_choice1) + \
            list(self.platform_choice2) + list(self.platform_choice3) + \
            list(self.platform_choice4) + list(self.platform_choice5)
        pf_set = set(pf_list)
        platform = list(pf_set)
        platform.sort()

    if state == 'final' and releasemessagereceipient is not None:
        api.portal.send_email(
            recipient=releasemessagereceipient,
            subject="New Release added",
            body=("""A new linked release was added and published with\n
                  title: {}\nURL: {}\nCompatibility:{}\n
                  Categories: {}\nLicenses: {}\n
                  Platforms: {}""").format(self.title,
                                           url,
                                           compatibility,
                                           category,
                                           licenses,
                                           platform),
        )

    else:
        return None


class ValidateEUpReleaseLinkUniqueness(validator.SimpleFieldValidator):
    # Validate site-wide uniqueness of release titles.

    def validate(self, value):
        # Perform the standard validation first
        super(ValidateEUpReleaseLinkUniqueness, self).validate(value)

        if value is not None:
            if IEUpReleaseLink.providedBy(self.context):
                # The release number is the same as the previous value stored
                # in the object
                if self.context.releasenumber == value:
                    return None

            catalog = api.portal.get_tool(name='portal_catalog')
            # Differentiate between possible contexts (on creation or editing)
            # on creation the context is the container
            # on editing the context is already the object
            if IEUpReleaseLink.providedBy(self.context):
                query = '/'.join(self.context.aq_parent.getPhysicalPath())
            else:
                query = '/'.join(self.context.getPhysicalPath())

            result = catalog({
                'path': {'query': query, 'depth': 1},
                'portal_type': ['tdf.extensionuploadcenter.euprelease',
                                'tdf.extensionuploadcenter.eupreleaselink'],
                'release_number': value})

            if len(result) > 0:
                raise Invalid(_(u"The release number is already in use. "
                                u"Please choose another one."))


validator.WidgetValidatorDiscriminators(
    ValidateEUpReleaseLinkUniqueness,
    field=IEUpReleaseLink['releasenumber'],
)


class EUpReleaseLinkView(DefaultView):
    def canPublishContent(self):
        return checkPermission('cmf.ModifyPortalContent', self.context)

    def releaseLicense(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        path = "/".join(self.context.getPhysicalPath())
        idx_data = catalog.getIndexDataForUID(path)
        licenses = idx_data.get('releaseLicense')
        return(r for r in licenses)

    def linkedreleaseCompatibility(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        path = "/".join(self.context.getPhysicalPath())
        idx_data = catalog.getIndexDataForUID(path)
        compatibility = idx_data.get('getCompatibility')
        return(r for r in compatibility)
